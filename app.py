from flask import Flask,render_template,request, redirect
from flask_bootstrap import Bootstrap
import os
from flask_sqlalchemy import SQLAlchemy



project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "urldatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


bootstrap=Bootstrap(app)


class url(db.Model):
    inputlink = db.Column(db.String(80), unique=True, primary_key=True)

    def __repr__(self):
        return "<urlink: {}>".format(self.inputlink)

@app.route("/", methods=["GET","POST"])
def main():
    global urls
    if request.form:
        u= url(inputlink=request.form.get("inputlink"))
        db.session.add(u)
        db.session.commit()
    urls=url.query.all()
    return render_template('base.html', urls=urls)

@app.route("/update", methods=["POST"])
def update():
    newurl=request.form.get("newurl")
    oldurl=request.form.get("oldurl")
    ur=url.query.filter_by(inputlink=oldurl).first()
    ur.inputlink=newurl
    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    inputlink=request.form.get("inputlink")
    ur=url.query.filter_by(inputlink=inputlink).first()
    db.session.delete(ur)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run()
