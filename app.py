from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open = StringField('Opening Time (e.g. 8AM)', validators=[DataRequired()])
    close = StringField('Closing Time (e.g. 5:30PM)', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating',
                                choices=[('1', '☕'), ('2', '☕☕'), ('3', '☕☕☕'), ('4', '☕☕☕☕'), ('5', '☕☕☕☕☕☕')],
                                validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Strength Rating',
                              choices=[('0', '✘'), ('1', '💪'), ('2', '💪💪'), ('3', '💪💪💪'), ('4', '💪💪💪💪'),
                                       ('5', '💪💪💪💪💪')], validators=[DataRequired()])
    power = SelectField('Power Socket Availability',
                        choices=[('0', '✘'), ('1', '🔌'), ('2', '🔌🔌'), ('3', '🔌🔌🔌'), ('4', '🔌🔌🔌🔌'), ('5', '🔌🔌🔌🔌🔌')],
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print(form.data)
        cafe_data = form.data.values()
        cafe_list = list(cafe_data)
        if int(cafe_list[4]) == 0:
            cafe_list[4] = '✘'
        else:
            cafe_list[4] = int(cafe_list[4]) * '☕'
        if int(cafe_list[5]) == 0:
            cafe_list[5] = '✘'
        else:
            cafe_list[5] = int(cafe_list[5]) * '💪'
        if int(cafe_list[6]) == 0:
            cafe_list[6] = '✘'
        else:
            cafe_list[6] = int(cafe_list[6]) * '🔌'
        append_cafe = ",".join(cafe_list[:7])
        with open("cafe-data.csv", "a") as file:
            file.write(f"\n{append_cafe}")
        return redirect(url_for('add_cafe'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run()
