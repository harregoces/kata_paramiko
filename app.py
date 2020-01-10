from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from SocketUtility import SocketUtility

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)


class Machines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String, unique=True, nullable=False)
    os = db.Column(db.String, nullable=True)
    ram = db.Column(db.String, nullable=True)
    rom = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Machine %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        ip = request.form['ip']
        port = request.form['port']
        username = request.form['username']
        password = request.form['password']
        socket_utility = SocketUtility(ip, port, username, password)
        os = socket_utility.get_os()
        ram = socket_utility.get_ram()
        rom = socket_utility.get_hard_disks()
        new_machine = Machines(ip=ip, os=os, ram=ram, rom=rom)
        try:
            db.session.add(new_machine)
            db.session.commit()
        except:
            return 'There was a problem'
    else:
        pass

    machines = Machines.query.order_by(Machines.id).all()
    return render_template('index.html', machines=machines)


@app.route('/delete/<int:id>')
def delete(id):
    machine_to_delete = Machines.query.get_or_404(id)
    try:
        db.session.delete(machine_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error'


if __name__ == '__main__':
    app.run(debug=True)
