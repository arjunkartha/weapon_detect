from flask import *
from database import *
import uuid
from vd_copy import *
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail
admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
	return render_template('adminhome.html')

@admin.route('/admin_managepolice',methods=['get','post'])
def admin_managepolice():
	data={}

	q="select * from police"
	res=select(q)
	data['police']=res

	if 'submit' in request.form:
		f=request.form['fname']
		l=request.form['lname']
		ph=request.form['phone']
		e=request.form['email']
		pl=request.form['place']
		u=request.form['username']
		pwd=request.form['password']
		q="insert  into login values(null,'%s','%s','police')" %(u,pwd)
		id=insert(q)
		q="insert into police values(null,'%s','%s','%s','%s','%s','%s')"%(id,f,l,pl,ph,e)
		insert(q)
		email = e

		pwd = "Username:" + u + "\nPassword:" + pwd

		
		try:
			gmail = smtplib.SMTP('smtp.gmail.com', 587)
			gmail.ehlo()
			gmail.starttls()
			gmail.login('pamuka16@gmail.com', 'qgun bywf bros hzbl')  
		except Exception as e:
			print("Couldn't setup email!!" + str(e))

		pwd = MIMEText(pwd)

		pwd['Subject'] = 'Your Login Details:'

		pwd['To'] = email

		pwd['From'] = 'pamuka16@gmail.com'

		try:
			gmail.send_message(pwd)

			flash("EMAIL SEND SUCCESFULLY")

		except Exception as e:
			print("COULDN'T SEND EMAIL", str(e))
		else:
			flash("INVALID DETAILS")
			flash('ADDED...')
		return redirect(url_for('admin.admin_managepolice'))



	if 'action' in request.args:
		action=request.args['action']
		pid=request.args['pid']

	else:
		action=None
	print(action)

	if action=="delete":
		q="delete from police where police_id='%s'"%(pid)
		delete(q)
		return redirect(url_for('admin.admin_managepolice'))


	if action=="update":
		q="select * from police where police_id='%s'"%(pid)
		res=select(q)
		data['policeupdate']=res



	if 'update' in request.form:
		f=request.form['fname']
		l=request.form['lname']
		ph=request.form['phone']
		e=request.form['email']
		pl=request.form['place']
		q="update police set fname='%s', lname='%s', phone='%s',email='%s',place='%s' where police_id='%s'"%(f,l,ph,e,pl,pid)
		update(q)



		return redirect(url_for('admin.admin_managepolice'))
	
	return render_template('admin_managepolice.html',data=data)


@admin.route('/admin_viewrequest',methods=['get','post'])
def admin_viewrequest():
	data={}
 
	q="select * from request inner join user using (user_id)"
	res=select(q)
	data['requestss']=res

	return render_template('admin_viewrequest.html',data=data)


@admin.route('/admin_viewlocation',methods=['get','post'])
def admin_viewlocation():
	data={}

	q="select * from location inner join user using (user_id)"
	res=select(q)
	data['location']=res

	return render_template('admin_viewlocation.html',data=data)


@admin.route('/admin_fileupload', methods=['GET', 'POST'])
def admin_fileupload():
    data = {}

    if request.method == 'POST':
        if 'video' not in request.files:
            flash('No video file uploaded')
            return redirect(request.url)
        video = request.files['video']
        if video.filename == '':
            flash('No selected video file')
            return redirect(request.url)
        if video:
            filename = str(uuid.uuid4()) + '_' + video.filename  # Generate a unique filename
            path = os.path.join('static', filename)
            video.save(path)
            q = "INSERT INTO `images` VALUES (null, '%s')" % path
            inserts(q)
            flash('Video uploaded successfully')
            return redirect(url_for('admin.admin_fileupload'))

    q = "SELECT * FROM images"
    res = select(q)
    data['img'] = res

    return render_template('admin_fileupload.html', data=data)

# @admin.route('/admin_fileupload', methods=['GET', 'POST'])
# def admin_fileupload():
#     data = {}

#     q = "SELECT * FROM images"
#     res = select(q)
#     data['img'] = res

#     if request.method == 'POST':
#         if 'video' not in request.files:
#             flash('No video file uploaded')
#             return redirect(request.url)
#         video = request.files['video']
#         if video.filename == '':
#             flash('No selected video file')
#             return redirect(request.url)
#         if video:
#             filename = 'uploaded_video.mp4'
#             video_path = os.path.join('images', filename)
#             video.save(video_path)
#             detect(video_path)  # Call the detect function on the uploaded video
#             return redirect(url_for('admin.admin_fileupload'))
    
#     return render_template('admin_fileupload.html', data=data)



		

@admin.route('/detection',methods=['get','post'])
def detection():
	detect()
	return render_template('adminhome.html')



@admin.route('/viewdetection',methods=['get','post'])
def viewdetection():
	data={}
	guy="select * from detect "
	data['view']=select(guy)
	return render_template('admin_viewdetection.html',data=data)


@admin.route('/admin_verify_user')
def admin_verify_user():
	data={}
	dd="SELECT * FROM `user`INNER JOIN `login`USING(`login_id`)"
	data['view_user']=select(dd)
	if 'action' in request.args:
		action=request.args['action']
		jj=request.args['jj']
	else:
		action=None
	if action=='accept':
		hh="update login set usertype='user' where login_id='%s' "%(jj)
		update(hh)
		return redirect(url_for('admin.admin_verify_user'))
	if action=='reject':
		hh="update login set usertype='reject' where login_id='%s' "%(jj)
		update(hh)
		return redirect(url_for('admin.admin_verify_user'))
	return render_template('admin_verify_user.html',data=data)



@admin.route('/updateloc',methods=['get','post'])
def updateloc():
	data={}
	did=request.args['did']
	if 'update' in request.form:
     
		lon=request.form['lon']
		lat=request.form['lat']

		up="update detect set latitude='%s', longitude='%s'  where detect_id='%s' "%(lat,lon,did)
		data['view']=update(up)
		return redirect(url_for('admin.viewdetection'))
 
	return render_template('update_loc.html',data=data)