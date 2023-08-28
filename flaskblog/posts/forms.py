from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    city = SelectField(
        "City",
        choices=[
            "San Francisco",
            "Seoul",
            "Taipei",
            "Hyderabad",
            "Buenos Aires",
            "London",
            "Berlin",
        ],
        coerce=str,
    )

    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")


class CommentForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")
