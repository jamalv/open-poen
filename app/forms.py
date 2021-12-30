from wtforms.fields.core import FieldList, FormField
from app import app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, Optional, URL, ValidationError
)
from wtforms.widgets import HiddenInput
from wtforms import (
    StringField, IntegerField, BooleanField, PasswordField, SubmitField,
    SelectField, TextAreaField, DecimalField, DateField, RadioField, Form
)
from wtforms.fields.html5 import EmailField

allowed_extensions = [
    'jpg', 'jpeg', 'png', 'txt', 'pdf', 'ods', 'xls', 'xlsx', 'odt', 'doc',
    'docx'
]


def validate_iban(form, field):
    if (field.data.startswith("NL") and field.data[4:7] == "BNG" and all([(x.isdigit()) for x in field.data[8:]])):
        return
    else:
        raise ValidationError(f"{field.data} is niet een BNG-rekening.")


class BNGLinkForm(FlaskForm):
    iban = StringField(
        "IBAN", validators=[DataRequired(), validate_iban]
    )
    valid_until = DateField(
        'Geldig tot', format="%d-%m-%Y",
        validators=[DataRequired()]
    )
    submit = SubmitField(
        'Aanmaken',
        render_kw={
            'class': 'btn btn-info'
        }
    )
    remove = SubmitField(
        'Verwijderen',
        render_kw={
            'class': 'btn btn-danger'
        }
    )


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(
        'E-mailadres', validators=[DataRequired(), Email(), Length(max=120)]
    )
    submit = SubmitField(
        'Bevestig',
        render_kw={
            'class': 'btn btn-info'
        }
    )


class ResetPasswordForm(FlaskForm):
    # Use 'Wachtwoord' instead of 'password' as the variable
    # is used in a user-facing error message when the passwords
    # don't match and we want it to show a Dutch word instead of
    # English
    Wachtwoord = PasswordField(
        'Wachtwoord',
        validators=[DataRequired(), Length(min=12)],
        render_kw={
            'autocomplete': 'new-password'
        }
    )
    Wachtwoord2 = PasswordField(
        'Herhaal wachtwoord',
        validators=[DataRequired(), EqualTo('Wachtwoord')],
        render_kw={
            'autocomplete': 'new-password'
        }
    )
    submit = SubmitField(
        'Bevestig',
        render_kw={
            'class': 'btn btn-info'
        }
    )


class LoginForm(FlaskForm):
    email = EmailField(
        'E-mailadres',
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    Wachtwoord = PasswordField(
        'Wachtwoord',
        validators=[DataRequired(), Length(min=12)],
        render_kw={
            'autocomplete': 'current-password'
        }
    )
    submit = SubmitField(
        'Inloggen',
        render_kw={
            'class': 'btn btn-info'
        }
    )


class NewProjectFunderForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired(), Length(max=120)])
    url = StringField(
        'URL', validators=[DataRequired(), URL(), Length(max=2000)]
    )


class CardNumber(FlaskForm):
    card_number = StringField("Pasnummer", validators=[DataRequired()])


class NewProjectSubprojectForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Beschrijving', validators=[DataRequired()])
    hidden = BooleanField('Initiatief verbergen')
    budget = IntegerField('Budget voor dit initiatief', validators=[Optional()])


class NewProjectForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Beschrijving', validators=[DataRequired()])
    contains_subprojects = BooleanField(
        'Uitgaven van dit project gebeuren via subrekeningen en subprojecten',
        render_kw={
            'checked': '',
            'value': 'y'
        }
    )
    hidden = BooleanField('Project verbergen')
    hidden_sponsors = BooleanField('Sponsoren verbergen')
    budget = IntegerField('Budget voor dit project', validators=[Optional()])
    card_numbers_amount = IntegerField("Aantal toe te voegen betaalpassen.", default=0)
    card_numbers = FieldList(
        FormField(CardNumber),
        min_entries=0,
        max_entries=None,
        validators=[]
    )
    funders_amount = IntegerField("Aantal toe te voegen sponsoren.", default=0)
    funders = FieldList(
        FormField(NewProjectFunderForm),
        min_entries=0,
        max_entries=None,
        validators=[]
    )
    subprojects_amount = IntegerField("Aantal toe te voegen initiatieven.", default=0)
    subprojects = FieldList(
        FormField(NewProjectSubprojectForm),
        min_entries=0,
        max_entries=None,
        validators=[]
    )
    id = IntegerField(widget=HiddenInput())
    submit = SubmitField(
        'Opslaan',
        render_kw={
            'class': 'btn btn-info'
        }
    )


class EditProjectForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Beschrijving', validators=[DataRequired()])
    contains_subprojects = BooleanField(
        'Uitgaven van dit project gebeuren via subrekeningen en subprojecten',
        render_kw={
            'checked': '',
            'value': 'y'
        }
    )
    hidden = BooleanField('Project verbergen')
    hidden_sponsors = BooleanField('Sponsoren verbergen')
    budget = IntegerField('Budget voor dit project', validators=[Optional()])
    id = IntegerField(widget=HiddenInput())
    submit = SubmitField(
        'Opslaan',
        render_kw={
            'class': 'btn btn-info'
        }
    )
    remove = SubmitField(
        'Verwijderen',
        render_kw={
            'class': 'btn btn-danger'
        }
    )


class SubprojectForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Beschrijving', validators=[DataRequired()])
    hidden = BooleanField('Initiatief verbergen')
    budget = IntegerField('Budget voor dit initiatief', validators=[Optional()])
    project_id = IntegerField(widget=HiddenInput())
    id = IntegerField(widget=HiddenInput())

    submit = SubmitField(
        'Opslaan',
        render_kw={
            'class': 'btn btn-info'
        }
    )

    remove = SubmitField(
        'Verwijderen',
        render_kw={
            'class': 'btn btn-danger'
        }
    )


# Allow both dot '.' and comma ',' as decimal separator
class FlexibleDecimalField(DecimalField):
    def process_formdata(self, valuelist):
        if valuelist:
            valuelist[0] = valuelist[0].replace(",", ".")
        return super(FlexibleDecimalField, self).process_formdata(valuelist)


# Add a new payment manually
class NewPaymentForm(FlaskForm):
    project_id = IntegerField(widget=HiddenInput(), validators=[Optional()])
    subproject_id = IntegerField(widget=HiddenInput(), validators=[Optional()])

    # Call the set_category function when the user selects a different
    # subproject (only on project pages) as we need to set new categories
    # that belong to that subproject
    subproject = SelectField(
        'Initiatief',
        coerce=int,
        choices=[],
        render_kw={'onchange': 'set_category(this)'}
    )

    category_id = SelectField('Categorie', validators=[Optional()], choices=[])

    route = SelectField(
        'Route',
        choices=[
            ('inkomsten', 'inkomsten'),
            ('inbesteding', 'inbesteding'),
            ('uitgaven', 'uitgaven')
        ]
    )

    amount_value = FlexibleDecimalField('Bedrag (begin met een "-" als het een uitgave is)')

    created = DateField('Datum (notatie: 31-12-2021)', format="%d-%m-%Y")

    alias_name = StringField(
        'Verstuurder naam', validators=[Length(max=120)]
    )
    alias_value = StringField(
        'Verstuurder IBAN', validators=[Length(max=120)]
    )

    counterparty_alias_name = StringField(
        'Ontvanger naam', validators=[Length(max=120)]
    )
    counterparty_alias_value = StringField(
        'Ontvanger IBAN', validators=[Length(max=120)]
    )

    short_user_description = StringField(
        'Korte beschrijving', validators=[Length(max=50)]
    )
    long_user_description = TextAreaField(
        'Lange beschrijving', validators=[Length(max=2000)]
    )

    hidden = BooleanField('Transactie verbergen')

    data_file = FileField(
        'Bestand',
        validators=[
            FileAllowed(
                allowed_extensions,
                (
                    'bestandstype niet toegstaan. Enkel de volgende '
                    'bestandstypen worden geaccepteerd: %s' % ', '.join(
                        allowed_extensions
                    )
                )
            ),
            Optional()
        ]
    )
    mediatype = RadioField(
        'Media type',
        choices=[
            ('media', 'media'),
            ('bon', 'bon')
        ],
        default="bon",
        validators=[Optional()]
    )

    submit = SubmitField(
        'Opslaan',
        render_kw={
            'class': 'btn btn-info'
        }
    )


# Edit a payment
class PaymentForm(FlaskForm):
    short_user_description = StringField(
        'Korte beschrijving', validators=[Length(max=50)]
    )
    long_user_description = TextAreaField(
        'Lange beschrijving', validators=[Length(max=2000)]
    )
    amount_value = FlexibleDecimalField('Bedrag (begin met een "-" als het een uitgave is)')
    created = DateField('Datum (notatie: 31-12-2020)', format="%d-%m-%Y")
    hidden = BooleanField('Transactie verbergen')
    category_id = SelectField('Categorie', validators=[Optional()], choices=[])
    route = SelectField('Route', choices=['inbesteding', 'uitgaven', 'inkomsten'])
    id = IntegerField(widget=HiddenInput())

    submit = SubmitField(
        'Opslaan',
        render_kw={
            'class': 'btn btn-info'
        }
    )

    # Only manually added payments are allowed to be removed
    remove = SubmitField(
        'Verwijderen',
        render_kw={
            'class': 'btn btn-danger'
        }
    )


class TransactionAttachmentForm(FlaskForm):
    data_file = FileField(
        'Bestand',
        validators=[
            FileRequired(),
            FileAllowed(
                allowed_extensions,
                (
                    'bestandstype niet toegstaan. Enkel de volgende '
                    'bestandstypen worden geaccepteerd: %s' % ', '.join(
                        allowed_extensions
                    )
                )
            )
        ]
    )
    mediatype = RadioField(
        'Media type',
        choices=[
            ('media', 'media'),
            ('bon', 'bon')
        ],
        default="bon",
        validators=[DataRequired()]
    )
    payment_id = IntegerField(widget=HiddenInput())
    submit = SubmitField(
        'Uploaden',
        render_kw={
            'class': 'btn btn-info'
        }
    )


class EditAttachmentForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    mediatype = RadioField(
        'Media type',
        choices=[
            ('media', 'media'),
            ('bon', 'bon')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField(
        'Opslaan',
        render_kw={
            'class': 'btn btn-info'
        }
    )

    remove = SubmitField(
        'Verwijderen',
        render_kw={
            'class': 'btn btn-danger'
        }
    )


class FunderForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired(), Length(max=120)])
    url = StringField(
        'URL', validators=[DataRequired(), URL(), Length(max=2000)]
    )
    id = IntegerField(widget=HiddenInput())

    submit = SubmitField(
        'Opslaan',
        render_kw={
            'class': 'btn btn-info'
        }
    )

    remove = SubmitField(
        'Verwijderen',
        render_kw={
            'class': 'btn btn-danger'
        }
    )


class AddUserForm(FlaskForm):
    email = StringField(
        'E-mailadres', validators=[DataRequired(), Email(), Length(max=120)]
    )
    admin = BooleanField(widget=HiddenInput())
    project_id = IntegerField(widget=HiddenInput())
    subproject_id = IntegerField(widget=HiddenInput())

    submit = SubmitField(
        'Uitnodigen',
        render_kw={
            'class': 'btn btn-info'
        }
    )


class EditAdminForm(FlaskForm):
    admin = BooleanField('Admin')
    active = BooleanField('Gebruikersaccount is actief')
    id = IntegerField(widget=HiddenInput())

    submit = SubmitField(
        'Opslaan',
        render_kw={
            'class': 'btn btn-info'
        }
    )


class EditProjectOwnerForm(FlaskForm):
    hidden = BooleanField('Project owner verbergen in initiatiefnemersoverzicht')
    remove_from_project = BooleanField(
        'Verwijder project owner van dit project'
    )
    active = BooleanField('Project owner account is actief')
    id = IntegerField(widget=HiddenInput())
    project_id = IntegerField(widget=HiddenInput())

    submit = SubmitField(
        'Opslaan',
        render_kw={
            'class': 'btn btn-info'
        }
    )


class EditUserForm(FlaskForm):
    hidden = BooleanField('Initiatiefnemer verbergen in initiatiefnemersoverzicht')
    remove_from_subproject = BooleanField(
        'Verwijder initiatiefnemer van dit project'
    )
    active = BooleanField('Initiatiefnemer account is actief')
    id = IntegerField(widget=HiddenInput())
    subproject_id = IntegerField(widget=HiddenInput())

    submit = SubmitField(
        'Opslaan',
        render_kw={
            'class': 'btn btn-info'
        }
    )


class EditProfileForm(FlaskForm):
    first_name = StringField(
        'Voornaam', validators=[DataRequired(), Length(max=120)]
    )
    last_name = StringField(
        'Achternaam', validators=[DataRequired(), Length(max=120)]
    )
    biography = TextAreaField(
        'Beschrijving', validators=[DataRequired(), Length(max=1000)]
    )

    allowed_extensions = [
        'jpg', 'jpeg', 'png'
    ]
    data_file = FileField(
        'Profielfoto (als u al een profielfoto heeft en een nieuwe toevoegt dan wordt de oude verwijderd)',
        validators=[
            FileAllowed(
                allowed_extensions,
                (
                    'bestandstype niet toegstaan. Enkel de volgende '
                    'bestandstypen worden geaccepteerd: %s' % ', '.join(
                        allowed_extensions
                    )
                )
            )
        ]
    )

    submit = SubmitField(
        'Opslaan',
        render_kw={
            'class': 'btn btn-info'
        }
    )


class CategoryForm(FlaskForm):
    name = StringField(
        'Naam', validators=[DataRequired(), Length(max=120)]
    )
    id = IntegerField(widget=HiddenInput())
    project_id = IntegerField(widget=HiddenInput())
    subproject_id = IntegerField(widget=HiddenInput())

    submit = SubmitField(
        'Opslaan',
        render_kw={
            'class': 'btn btn-info'
        }
    )

    remove = SubmitField(
        'Verwijderen',
        render_kw={
            'class': 'btn btn-danger'
        }
    )
