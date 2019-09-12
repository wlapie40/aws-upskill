from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Response,
    session,
)
from flask_login import (login_user,
                         login_required,
                         logout_user,
                         current_user, )
from werkzeug.security import generate_password_hash, check_password_hash

from api.api import (ListS3Buckets,
                     ListS3BucketFiles,
                     DeleteS3BucketFile,
                     UploadS3BucketFile,
                     DownloadS3BucketFile,
                     )
from database import create_app
from forms import (LoginForm,
                   RegisterForm,
                   NewBucketForm,
                   )
from models import db, User
from resources import (get_bucket,
                       get_buckets_list,
                       get_region_name,
                       _get_s3_resource,
                       _get_cloud_watch_logs,
                       )

app, api, login_manager, cur_env, cw_log = create_app()

#  todo create a separate class to keep details about logged user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        bucket = request.form['bucket']
        session['bucket'] = bucket
        return redirect(url_for('files'))
    else:
        buckets = get_buckets_list()
        # cw_log.put_log_events(message=f'ROUTE--> index TOP 10 {buckets[:10]}')
        return render_template("index.html", buckets=buckets, name=current_user.username, cur_env=cur_env)


@app.route('/files')
@login_required
def files():
    buckets = get_bucket()
    summaries = buckets.objects.all()
    try:
        # cw_log.put_log_events(message=f'ROUTE--> FILES msg: buckets:{buckets} summaries:{summaries}')
        return render_template('files.html', my_bucket=buckets,
                               files=summaries, name=current_user.username, cur_env=cur_env)
    except:
        return render_template("index.html", buckets=buckets, name=current_user.username, cur_env=cur_env)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    my_bucket = get_bucket()
    my_bucket.Object(file.filename).put(Body=file)

    # cw_log.put_log_events(message=f'ROUTE--> UPLOAD msg: "{file.filename}" uploaded successfully')
    flash('File uploaded successfully')
    return redirect(url_for('files'))


@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    # cw_log.put_log_events(message=f'ROUTE--> delete msg:File: {key} deleted')
    flash('File deleted successfully')
    return redirect(url_for('files'))


@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']
    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()

    # cw_log.put_log_events(message=f'ROUTE--> download msg:File: {key} downloaded')
    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )


@app.route('/login2', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password)
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('User has already been created')
            return redirect(url_for('signup'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/create_bucket', methods=['GET', 'POST'])
@login_required
def create_bucket():
    form = NewBucketForm()
    if form.validate_on_submit():
        current_region = get_region_name()
        bucket_name = str(form.bucket_name.data)
        s3_resource = _get_s3_resource()

        s3_resource.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': current_region})

    else:
        return render_template('create_bucket.html', form=form, name=current_user.username, cur_env=cur_env)
    # cw_log.put_log_events(message=f'ROUTE--> create_bucket msg: bucket {bucket_name}{current_region} has been created')
    return render_template('create_bucket.html', form=form, name=current_user.username, cur_env=cur_env)


@app.route('/instance/monitoring', methods=['GET', 'POST'])
@login_required
def cloud_watch():
    response = _get_cloud_watch_logs(cw_log.log_group_name)
    # cw_log.put_log_events(message=f'ROUTE--> cloud_watch')
    return render_template('instance_monitoring.html', logs=response['events'],
                           name=current_user.username, cur_env=cur_env)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # cw_log.put_log_events(message=f'ROUTE--> logout LOG OUT')
    return redirect(url_for('index'))


api.add_resource(ListS3Buckets,
                 '/list/api/v1.0/buckets')
api.add_resource(ListS3BucketFiles,
                 '/list/api/v1.0/buckets/files')
api.add_resource(DeleteS3BucketFile,
                 '/delete/api/v1.0/file')
api.add_resource(UploadS3BucketFile,
                 '/upload/api/v1.0/file')
api.add_resource(DownloadS3BucketFile,
                 '/download/api/v1.0/file')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
