from flask import Flask, render_template,request,redirect, url_for,flash,make_response
import os
from gevent import pywsgi
from flask import jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from pyngrok import ngrok

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:\\try_on_web\\Web_app\\merchant_images.db'  # 商家数据库
app.config['SQLALCHEMY_BINDS'] = {
    'customer': 'sqlite:///E:\\try_on_web\\Web_app\\customer_images.db'  # 顾客数据库
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # 用于支持 flash 消息

# 初始化数据库
db = SQLAlchemy(app)
# 商家图像模型
# 商家图像模型
class MerchantImage(db.Model):
    __tablename__ = 'merchant_images'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    label = db.Column(db.String(20), nullable=False)  # 添加标签

class CustomerImage(db.Model):
    __tablename__ = 'customer_images'
    __bind_key__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    label = db.Column(db.String(20), nullable=False)  # 添加标签



with app.app_context():
    #db.drop_all()
    db.create_all()  # 创建默认数据库表
    #db.create_all(bind_key=app.config['SQLALCHEMY_BINDS']['customer'])
    db.create_all(bind_key='customer')  # 创建顾客数据库表



@app.route('/Try_on_program')
def Try_on_program():
    return 'Hello Try_on_program!'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/data')
def about():
    return render_template('data.html')


@app.route('/about')
def posts():
    return render_template('about.html')

@app.route('/wardrobe_magic', methods=['GET', 'POST'])
def wardrobe_magic():
    if request.method == 'POST':
        image_file = request.files.get('image')
        label = request.form.get('label')

        if image_file and label:
            filename = secure_filename(image_file.filename)
            image_data = image_file.read()

            # 按标签存入不同数据库
            if label == '衣物':
                new_image = MerchantImage(filename=filename, data=image_data,label=label)
                db.session.add(new_image)
            elif label == '人像':
                new_image = CustomerImage(filename=filename, data=image_data,label=label)
                db.session.add(new_image)

            db.session.commit()
            flash('上传成功！')
            print(f"[DEBUG] 上传标签为：{label}")

            return redirect(url_for('wardrobe_magic'))
        else:
            flash('请上传图片并选择标签。')

    return render_template('wardrobe_magic.html')


@app.route('/infinite_wardrobe')
def infinite_wardrobe():
    images = MerchantImage.query.filter_by(label='衣物').all()
    return render_template('infinite_wardrobe.html', images=images)

@app.route('/magic_camera')
def magic_camera():
    images = CustomerImage.query.filter_by(label='人像').all()
    return render_template('magic_camera.html', images=images)


@app.route('/magic_mirror')
def magic_mirror():
    return render_template('magic_mirror.html')

@app.route('/view_image/<int:image_id>')
def view_image(image_id):
    image = MerchantImage.query.get_or_404(image_id)
    response = make_response(image.data)
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@app.route('/view_customer_image/<int:image_id>')
def view_customer_image(image_id):
    image = CustomerImage.query.get_or_404(image_id)
    response = make_response(image.data)
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@app.route('/delete_image/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    image = MerchantImage.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    flash('衣物图片已删除')
    return redirect(url_for('infinite_wardrobe'))

@app.route('/delete_customer_image/<int:image_id>', methods=['POST'])
def delete_customer_image(image_id):
    image = CustomerImage.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    flash('人像图片已删除')
    return redirect(url_for('magic_camera'))
if __name__ == '__main__':
    #======先启动 ngrok，把本地 5000 端口映射到公网======
    public_url = ngrok.connect(5000)  # 默认 http，也可以 ngrok.connect(5000, "http")
    print(" * Public URL:", public_url)

    #=====启动Flask=====
    app.run(host='0.0.0.0')

