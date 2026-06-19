import json
import tempfile
import shutil

from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import LoanApplication, ClientProfile, AnalystProfile, AnalystNote, Document


# ============================================================
# HELPERS
# ============================================================

def create_client_user(email="client@test.com", password="testpass123"):
    user = User.objects.create_user(
        username=email, email=email, password=password,
        first_name="John", last_name="Doe", is_staff=False
    )
    ClientProfile.objects.create(user=user)
    return user


def create_analyst_user(email="analyst@test.com", password="testpass123"):
    user = User.objects.create_user(
        username=email, email=email, password=password,
        first_name="Jane", last_name="Smith", is_staff=True
    )
    AnalystProfile.objects.create(user=user)
    return user


def create_application(user, **kwargs):
    defaults = dict(
        age=35, income=75000, experience=10,
        current_house_yrs=5, cur_job_years=4,
        loan_amount=15000,
        marital_status='married', house_ownership='owned',
        car_ownership='yes', region='South India',
        job_category='Engineering',
        risk_score=25.0, risk_flag=0, ai_prediction='Approved'
    )
    defaults.update(kwargs)
    return LoanApplication.objects.create(user=user, **defaults)


VALID_APPLICATION_DATA = {
    'loan_amount': 15000,
    'age': 35,
    'income': 75000,
    'experience': 10,
    'current_house_yrs': 5,
    'cur_job_years': 4,
    'marital_status': 'married',
    'house_ownership': 'owned',
    'car_ownership': 'yes',
    'region': 'South India',
    'job_category': 'Engineering',
}

VALID_API_DATA = {
    'age': 35,
    'income': 75000,
    'experience': 10,
    'current_house_yrs': 5,
    'cur_job_years': 4,
    'marital_status': 'married',
    'house_ownership': 'owned',
    'car_ownership': 'yes',
    'region': 'South India',
    'job_category': 'Engineering',
}


# ============================================================
# 1. TESTS D'INSCRIPTION
# ============================================================

class RegistrationTests(TestCase):

    def test_register_new_user_success(self):
        """Un nouvel utilisateur peut créer un compte."""
        response = self.client.post(reverse('register'), {
            'first_name': 'Alice',
            'last_name': 'Martin',
            'email': 'alice@test.com',
            'password': 'securepass123',
            'confirm_password': 'securepass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='alice@test.com').exists())
        self.assertTrue(ClientProfile.objects.filter(user__username='alice@test.com').exists())

    def test_register_existing_email_shows_error(self):
        """Un email déjà utilisé affiche un message d'erreur."""
        create_client_user(email='existing@test.com')
        response = self.client.post(reverse('register'), {
            'first_name': 'Bob',
            'last_name': 'Dupont',
            'email': 'existing@test.com',
            'password': 'securepass123',
            'confirm_password': 'securepass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(first_name='Bob').exists())

    def test_register_password_mismatch_fails(self):
        """Des mots de passe différents empêchent la création du compte."""
        response = self.client.post(reverse('register'), {
            'first_name': 'Carol',
            'last_name': 'Test',
            'email': 'carol@test.com',
            'password': 'password123',
            'confirm_password': 'different456',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='carol@test.com').exists())


# ============================================================
# 2. TESTS DE CONNEXION
# ============================================================

class LoginTests(TestCase):

    def setUp(self):
        self.user = create_client_user()

    def test_login_valid_credentials(self):
        """Un utilisateur peut se connecter avec des identifiants valides."""
        response = self.client.post(reverse('login'), {
            'email': 'client@test.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_wrong_password(self):
        """Un mauvais mot de passe empêche la connexion."""
        response = self.client.post(reverse('login'), {
            'email': 'client@test.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_unknown_email(self):
        """Un email inconnu empêche la connexion."""
        response = self.client.post(reverse('login'), {
            'email': 'unknown@test.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects_to_login(self):
        """La déconnexion redirige vers la page de login."""
        self.client.login(username='client@test.com', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))


# ============================================================
# 3. TESTS D'ACCÈS SÉCURISÉ
# ============================================================

class AccessControlTests(TestCase):

    def setUp(self):
        self.client_user = create_client_user()
        self.analyst_user = create_analyst_user()

    def test_dashboard_requires_login(self):
        """Le dashboard client nécessite d'être connecté."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_client_cannot_access_analyst_dashboard(self):
        """Un client ne peut pas accéder au dashboard analyste."""
        self.client.login(username='client@test.com', password='testpass123')
        response = self.client.get(reverse('analyst_dashboard'))
        self.assertRedirects(response, reverse('login'))

    def test_analyst_can_access_analyst_dashboard(self):
        """Un analyste peut accéder au dashboard analyste."""
        self.client.login(username='analyst@test.com', password='testpass123')
        response = self.client.get(reverse('analyst_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_cannot_access_apply(self):
        """Un utilisateur non connecté ne peut pas soumettre de demande."""
        response = self.client.get(reverse('apply_loan'))
        self.assertEqual(response.status_code, 302)

    def test_analyst_login_with_client_credentials_denied(self):
        """Un client ne peut pas se connecter via le portail analyste."""
        response = self.client.post(reverse('analyst_login'), {
            'email': 'client@test.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)


# ============================================================
# 4. TESTS DE L'API
# ============================================================

class PredictAPITests(TestCase):

    def test_api_valid_data_returns_200(self):
        """L'API retourne 200 avec des données valides."""
        response = self.client.post(
            reverse('api_predict'),
            data=VALID_API_DATA,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('probability', data)
        self.assertIn('decision', data)

    def test_api_probability_between_0_and_100(self):
        """La probabilité retournée est entre 0 et 100."""
        response = self.client.post(
            reverse('api_predict'),
            data=VALID_API_DATA,
            content_type='application/json'
        )
        data = response.json()
        self.assertGreaterEqual(data['probability'], 0)
        self.assertLessEqual(data['probability'], 100)

    def test_api_decision_is_valid_choice(self):
        """La décision retournée est Approved, Pending ou Rejected."""
        response = self.client.post(
            reverse('api_predict'),
            data=VALID_API_DATA,
            content_type='application/json'
        )
        data = response.json()
        self.assertIn(data['decision'], ['Approved', 'Pending', 'Rejected'])

    def test_api_missing_field_returns_400(self):
        """Un champ manquant retourne une erreur 400."""
        incomplete_data = VALID_API_DATA.copy()
        del incomplete_data['age']
        response = self.client.post(
            reverse('api_predict'),
            data=incomplete_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_api_invalid_marital_status_returns_400(self):
        """Une valeur invalide pour marital_status retourne 400."""
        invalid_data = VALID_API_DATA.copy()
        invalid_data['marital_status'] = 'divorced'
        response = self.client.post(
            reverse('api_predict'),
            data=invalid_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_api_get_method_not_allowed(self):
        """L'API n'accepte pas les requêtes GET."""
        response = self.client.get(reverse('api_predict'))
        self.assertEqual(response.status_code, 405)


# ============================================================
# 5. TESTS DE DEMANDE DE PRÊT (flux en 2 étapes)
# ============================================================

class LoanApplicationTests(TestCase):
    """
    Le flux réel est en 2 étapes :
      1. POST /apply/       → valide le formulaire, stocke en session, redirige vers /apply/review/
      2. POST /apply/review/ → crée l'application en BDD, lance l'IA, redirige vers /success/
    Les anciens tests postaient directement sur /apply/ et vérifiaient la BDD,
    ce qui ne pouvait jamais fonctionner car la création a lieu dans review_loan.
    """

    def setUp(self):
        self.user = create_client_user()
        self.client.login(username='client@test.com', password='testpass123')

    def _submit_application(self, data=None):
        """Simule le flux complet : formulaire → révision → soumission."""
        self.client.post(reverse('apply_loan'), data or VALID_APPLICATION_DATA)
        return self.client.post(reverse('review_loan'))

    # --- Cas nominal ---

    def test_apply_valid_data_creates_application(self):
        """Une demande valide complète crée bien une application en base."""
        self._submit_application()
        self.assertEqual(LoanApplication.objects.filter(user=self.user).count(), 1)

    def test_apply_sets_ai_prediction(self):
        """Le modèle IA assigne bien une prédiction après soumission."""
        self._submit_application()
        app = LoanApplication.objects.filter(user=self.user).first()
        self.assertIn(app.ai_prediction, ['Approved', 'Pending', 'Rejected'])

    def test_apply_sets_risk_score(self):
        """Le risk_score est bien calculé et entre 0 et 100."""
        self._submit_application()
        app = LoanApplication.objects.filter(user=self.user).first()
        self.assertIsNotNone(app.risk_score)
        self.assertGreaterEqual(app.risk_score, 0)
        self.assertLessEqual(app.risk_score, 100)

    def test_apply_final_decision_is_null_by_default(self):
        """La décision finale est null par défaut — en attente de l'analyste."""
        self._submit_application()
        app = LoanApplication.objects.filter(user=self.user).first()
        self.assertIsNone(app.final_decision)

    def test_apply_redirects_to_success(self):
        """La confirmation redirige vers la page de succès."""
        self.client.post(reverse('apply_loan'), VALID_APPLICATION_DATA)
        response = self.client.post(reverse('review_loan'))
        self.assertRedirects(response, reverse('success_page'))

    def test_apply_step1_redirects_to_review(self):
        """La soumission du formulaire redirige vers la page de révision."""
        response = self.client.post(reverse('apply_loan'), VALID_APPLICATION_DATA)
        self.assertRedirects(response, reverse('review_loan'))

    def test_review_without_session_redirects_to_apply(self):
        """Accéder à la page de révision sans session redirige vers le formulaire."""
        response = self.client.get(reverse('review_loan'))
        self.assertRedirects(response, reverse('apply_loan'))

    # --- Validations métier ---

    def test_experience_cannot_exceed_age_minus_18(self):
        """L'expérience ne peut pas dépasser age - 18."""
        invalid_data = VALID_APPLICATION_DATA.copy()
        invalid_data['age'] = 20
        invalid_data['experience'] = 10  # max autorisé = 2
        response = self.client.post(reverse('apply_loan'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LoanApplication.objects.filter(user=self.user).count(), 0)

    def test_cur_job_years_cannot_exceed_experience(self):
        """Les années dans le job actuel ne peuvent pas dépasser l'expérience."""
        invalid_data = VALID_APPLICATION_DATA.copy()
        invalid_data['experience'] = 3
        invalid_data['cur_job_years'] = 8
        response = self.client.post(reverse('apply_loan'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LoanApplication.objects.filter(user=self.user).count(), 0)

    def test_income_must_be_positive(self):
        """Le revenu doit être supérieur à 0."""
        invalid_data = VALID_APPLICATION_DATA.copy()
        invalid_data['income'] = 0
        response = self.client.post(reverse('apply_loan'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LoanApplication.objects.filter(user=self.user).count(), 0)

    def test_loan_amount_minimum(self):
        """Le montant du prêt doit être au moins 1000."""
        invalid_data = VALID_APPLICATION_DATA.copy()
        invalid_data['loan_amount'] = 500
        response = self.client.post(reverse('apply_loan'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LoanApplication.objects.filter(user=self.user).count(), 0)

    def test_house_years_cannot_exceed_age(self):
        """Les années à l'adresse actuelle ne peuvent pas dépasser l'âge."""
        invalid_data = VALID_APPLICATION_DATA.copy()
        invalid_data['age'] = 22
        invalid_data['experience'] = 4
        invalid_data['cur_job_years'] = 2
        invalid_data['current_house_yrs'] = 30  # impossible à 22 ans
        response = self.client.post(reverse('apply_loan'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LoanApplication.objects.filter(user=self.user).count(), 0)


# ============================================================
# 6. TESTS DES ACTIONS ANALYSTE
# ============================================================

class AnalystActionsTests(TestCase):

    def setUp(self):
        self.client_user = create_client_user()
        self.analyst_user = create_analyst_user()
        self.application = create_application(self.client_user)

    def _login_analyst(self):
        self.client.login(username='analyst@test.com', password='testpass123')

    # --- Approbation / Rejet via JSON ---

    def test_analyst_can_approve_via_json(self):
        """L'analyste peut approuver une demande via l'endpoint JSON."""
        self._login_analyst()
        response = self.client.post(
            reverse('analyst_update_status', args=[self.application.id]),
            data=json.dumps({'status': 'Approved'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.application.refresh_from_db()
        self.assertEqual(self.application.final_decision, 'Approved')

    def test_analyst_can_reject_via_json(self):
        """L'analyste peut rejeter une demande via l'endpoint JSON."""
        self._login_analyst()
        self.client.post(
            reverse('analyst_update_status', args=[self.application.id]),
            data=json.dumps({'status': 'Rejected'}),
            content_type='application/json'
        )
        self.application.refresh_from_db()
        self.assertEqual(self.application.final_decision, 'Rejected')

    def test_analyst_update_status_invalid_value_returns_400(self):
        """Un statut invalide retourne une erreur 400."""
        self._login_analyst()
        response = self.client.post(
            reverse('analyst_update_status', args=[self.application.id]),
            data=json.dumps({'status': 'Maybe'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_client_cannot_update_status(self):
        """Un client ne peut pas modifier le statut d'une demande."""
        self.client.login(username='client@test.com', password='testpass123')
        response = self.client.post(
            reverse('analyst_update_status', args=[self.application.id]),
            data=json.dumps({'status': 'Approved'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    # --- Approbation / Rejet via formulaire ---

    def test_analyst_can_update_status_via_form(self):
        """L'analyste peut modifier le statut via le formulaire."""
        self._login_analyst()
        self.client.post(
            reverse('analyst_update_status_form', args=[self.application.id]),
            {'status': 'Rejected'}
        )
        self.application.refresh_from_db()
        self.assertEqual(self.application.final_decision, 'Rejected')

    def test_client_cannot_update_status_via_form(self):
        """Un client est redirigé s'il tente de modifier le statut via le formulaire."""
        self.client.login(username='client@test.com', password='testpass123')
        response = self.client.post(
            reverse('analyst_update_status_form', args=[self.application.id]),
            {'status': 'Approved'}
        )
        self.assertRedirects(response, reverse('login'))
        self.application.refresh_from_db()
        self.assertIsNone(self.application.final_decision)

    # --- Notes ---

    def test_analyst_can_add_note(self):
        """L'analyste peut ajouter une note sur une demande."""
        self._login_analyst()
        self.client.post(
            reverse('analyst_application_detail', args=[self.application.id]),
            {'action': 'add_note', 'comment': 'Documents manquants.'}
        )
        self.assertEqual(AnalystNote.objects.filter(application=self.application).count(), 1)
        note = AnalystNote.objects.get(application=self.application)
        self.assertEqual(note.comment, 'Documents manquants.')

    def test_empty_note_is_not_saved(self):
        """Une note vide n'est pas enregistrée."""
        self._login_analyst()
        self.client.post(
            reverse('analyst_application_detail', args=[self.application.id]),
            {'action': 'add_note', 'comment': ''}
        )
        self.assertEqual(AnalystNote.objects.filter(application=self.application).count(), 0)

    # --- Déconnexion ---

    def test_analyst_logout_redirects(self):
        """La déconnexion analyste redirige vers la page de login analyste."""
        self._login_analyst()
        response = self.client.get(reverse('analyst_logout'))
        self.assertRedirects(response, reverse('analyst_login'))


# ============================================================
# 7. TESTS DU DASHBOARD ET DES MESSAGES CLIENT
# ============================================================

class ClientDashboardTests(TestCase):

    def setUp(self):
        self.user = create_client_user()
        self.analyst_user = create_analyst_user()
        self.client.login(username='client@test.com', password='testpass123')
        self.application = create_application(self.user)

    def test_dashboard_shows_own_applications(self):
        """Le dashboard affiche les demandes de l'utilisateur connecté."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.application, response.context['applications'])

    def test_dashboard_does_not_show_other_users_applications(self):
        """Le dashboard n'affiche pas les demandes d'autres utilisateurs."""
        other_user = create_client_user(email='other@test.com')
        other_app = create_application(
            other_user,
            marital_status='single', house_ownership='rented',
            car_ownership='no', region='North India',
            job_category='Technology & IT',
            risk_score=60.0, risk_flag=1, ai_prediction='Pending'
        )
        response = self.client.get(reverse('dashboard'))
        self.assertNotIn(other_app, response.context['applications'])

    def test_dashboard_shows_unread_count(self):
        """Le dashboard affiche le compteur de messages non lus."""
        AnalystNote.objects.create(
            application=self.application,
            analyst=self.analyst_user,
            comment="Merci de fournir un justificatif.",
            is_read=False
        )
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.context['unread_count'], 1)

    def test_messages_view_shows_notes(self):
        """La vue messages affiche les notes de l'analyste."""
        AnalystNote.objects.create(
            application=self.application,
            analyst=self.analyst_user,
            comment="Votre dossier est en cours d'examen.",
            is_read=False
        )
        response = self.client.get(reverse('messages'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('notes', response.context)
        self.assertEqual(response.context['notes'].count(), 1)

    def test_messages_view_marks_notes_as_read(self):
        """Consulter les messages marque les notes non lues comme lues."""
        note = AnalystNote.objects.create(
            application=self.application,
            analyst=self.analyst_user,
            comment="Votre dossier est en cours d'examen.",
            is_read=False
        )
        self.client.get(reverse('messages'))
        note.refresh_from_db()
        self.assertTrue(note.is_read)

    def test_unread_count_endpoint_returns_correct_value(self):
        """L'endpoint unread_count retourne le bon compteur JSON."""
        AnalystNote.objects.create(
            application=self.application, analyst=self.analyst_user,
            comment="Note 1", is_read=False
        )
        AnalystNote.objects.create(
            application=self.application, analyst=self.analyst_user,
            comment="Note 2", is_read=False
        )
        response = self.client.get(reverse('unread_count'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_unread_count_excludes_read_notes(self):
        """L'endpoint unread_count n'inclut pas les notes déjà lues."""
        AnalystNote.objects.create(
            application=self.application, analyst=self.analyst_user,
            comment="Note lue", is_read=True
        )
        response = self.client.get(reverse('unread_count'))
        self.assertEqual(response.json()['count'], 0)

    def test_success_page_shows_last_application(self):
        """La page de succès affiche la dernière demande soumise."""
        response = self.client.get(reverse('success_page'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['application'], self.application)


# ============================================================
# 8. TESTS D'UPLOAD DE DOCUMENTS
# ============================================================

TEMP_MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class DocumentUploadTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.user = create_client_user()
        self.client.login(username='client@test.com', password='testpass123')

    def test_document_uploaded_with_application(self):
        """Les documents uploadés sont bien liés à la demande créée."""
        self.client.post(reverse('apply_loan'), VALID_APPLICATION_DATA)
        fake_file = SimpleUploadedFile("payslip.pdf", b"PDF content", content_type="application/pdf")
        self.client.post(reverse('review_loan'), {
            'documents': fake_file,
            'document_types': 'payslip',
        })
        app = LoanApplication.objects.filter(user=self.user).first()
        self.assertIsNotNone(app)
        self.assertEqual(app.documents.count(), 1)
        self.assertEqual(app.documents.first().document_type, 'payslip')

    def test_application_created_without_documents(self):
        """Une demande peut être soumise sans documents joints."""
        self.client.post(reverse('apply_loan'), VALID_APPLICATION_DATA)
        self.client.post(reverse('review_loan'))
        app = LoanApplication.objects.filter(user=self.user).first()
        self.assertIsNotNone(app)
        self.assertEqual(app.documents.count(), 0)


# ============================================================
# 9. TESTS DES MODÈLES
# ============================================================

class ModelTests(TestCase):

    def setUp(self):
        self.user = create_client_user()
        self.analyst_user = create_analyst_user()
        self.application = create_application(self.user)

    def test_loan_application_reference_format(self):
        """La propriété reference suit le format APP-YYYY-XXXXXX."""
        ref = self.application.reference
        self.assertTrue(ref.startswith('APP-'))
        parts = ref.split('-')
        self.assertEqual(len(parts), 3)
        self.assertTrue(parts[1].isdigit())
        self.assertEqual(len(parts[2]), 6)

    def test_analyst_note_default_is_unread(self):
        """Une nouvelle note est non lue par défaut."""
        note = AnalystNote.objects.create(
            application=self.application,
            analyst=self.analyst_user,
            comment="Test note"
        )
        self.assertFalse(note.is_read)

    def test_analyst_note_linked_to_application(self):
        """Une note est correctement liée à sa demande via related_name."""
        AnalystNote.objects.create(
            application=self.application,
            analyst=self.analyst_user,
            comment="Vérification effectuée."
        )
        self.assertEqual(self.application.notes.count(), 1)

    def test_loan_application_str(self):
        """Le __str__ d'une demande contient l'ID et le risk_flag."""
        result = str(self.application)
        self.assertIn(str(self.application.id), result)
        self.assertIn(str(self.application.risk_flag), result)


# ============================================================
# 10. TESTS DE GESTION DU PROFIL
# ============================================================

class ProfileTests(TestCase):

    def setUp(self):
        self.user = create_client_user()
        self.client.login(username='client@test.com', password='testpass123')

    def test_profile_page_requires_login(self):
        """La page profil nécessite d'être connecté."""
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_page_displays_user_info(self):
        """La page profil affiche les informations de l'utilisateur."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')
        self.assertContains(response, 'Doe')

    def test_profile_form_prefilled_with_current_data(self):
        """Le formulaire est pré-rempli avec les données actuelles."""
        response = self.client.get(reverse('profile'))
        form = response.context['form']
        self.assertEqual(form.initial['first_name'], 'John')
        self.assertEqual(form.initial['last_name'], 'Doe')
        self.assertEqual(form.initial['email'], 'client@test.com')

    def test_update_name_success(self):
        """L'utilisateur peut modifier son nom."""
        self.client.post(reverse('profile'), {
            'first_name': 'Johnny',
            'last_name': 'Updated',
            'email': 'client@test.com',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Johnny')
        self.assertEqual(self.user.last_name, 'Updated')

    def test_update_email_success(self):
        """L'utilisateur peut modifier son email."""
        self.client.post(reverse('profile'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newemail@test.com',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@test.com')
        self.assertEqual(self.user.username, 'newemail@test.com')

    def test_update_email_duplicate_rejected(self):
        """Un email déjà utilisé par un autre compte est refusé."""
        create_client_user(email='taken@test.com')
        response = self.client.post(reverse('profile'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'taken@test.com',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'client@test.com')

    def test_update_password_success(self):
        """L'utilisateur peut changer son mot de passe."""
        self.client.post(reverse('profile'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'client@test.com',
            'new_password': 'newsecure456',
            'confirm_new_password': 'newsecure456',
        })
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newsecure456'))

    def test_update_password_mismatch_rejected(self):
        """Des mots de passe différents empêchent le changement."""
        response = self.client.post(reverse('profile'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'client@test.com',
            'new_password': 'newsecure456',
            'confirm_new_password': 'different789',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('testpass123'))

    def test_update_password_too_short_rejected(self):
        """Un mot de passe trop court est refusé."""
        response = self.client.post(reverse('profile'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'client@test.com',
            'new_password': 'short',
            'confirm_new_password': 'short',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('testpass123'))

    def test_blank_password_keeps_current(self):
        """Laisser le mot de passe vide conserve l'ancien."""
        self.client.post(reverse('profile'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'client@test.com',
            'new_password': '',
            'confirm_new_password': '',
        })
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('testpass123'))


class DeleteAccountTests(TestCase):

    def setUp(self):
        self.user = create_client_user()
        self.client.login(username='client@test.com', password='testpass123')

    def test_delete_account_requires_login(self):
        """La suppression de compte nécessite d'être connecté."""
        self.client.logout()
        response = self.client.post(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='client@test.com').exists())

    def test_delete_account_removes_user(self):
        """La suppression supprime bien l'utilisateur de la base."""
        self.client.post(reverse('delete_account'))
        self.assertFalse(User.objects.filter(username='client@test.com').exists())

    def test_delete_account_removes_applications(self):
        """La suppression supprime aussi les demandes de prêt associées."""
        create_application(self.user)
        self.client.post(reverse('delete_account'))
        self.assertEqual(LoanApplication.objects.filter(user=self.user).count(), 0)

    def test_delete_account_redirects_to_login(self):
        """Après suppression, l'utilisateur est redirigé vers le login."""
        response = self.client.post(reverse('delete_account'))
        self.assertRedirects(response, reverse('login'))

    def test_delete_account_get_redirects_to_profile(self):
        """Un GET sur delete_account redirige vers le profil (pas de suppression)."""
        response = self.client.get(reverse('delete_account'))
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(User.objects.filter(username='client@test.com').exists())


# ============================================================
# 11. TESTS DE SECURITE
# ============================================================

class SecurityTests(TestCase):

    def setUp(self):
        self.client_user = create_client_user()
        self.analyst_user = create_analyst_user()
        self.application = create_application(self.client_user)

    # --- CSRF ---

    def test_login_post_without_csrf_fails(self):
        """Un POST sans token CSRF est rejeté."""
        from django.test import Client
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(reverse('login'), {
            'email': 'client@test.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 403)

    def test_register_post_without_csrf_fails(self):
        """L'inscription sans token CSRF est rejetée."""
        from django.test import Client
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(reverse('register'), {
            'first_name': 'Test', 'last_name': 'User',
            'email': 'test@csrf.com',
            'password': 'securepass123',
            'confirm_password': 'securepass123',
        })
        self.assertEqual(response.status_code, 403)

    # --- XSS Prevention ---

    def test_xss_in_first_name_is_escaped(self):
        """Du HTML injecté dans le prénom est échappé à l'affichage."""
        self.client_user.first_name = '<script>alert("xss")</script>'
        self.client_user.save()
        self.client.login(username='client@test.com', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertNotContains(response, '<script>alert("xss")</script>')
        self.assertContains(response, '&lt;script&gt;')

    def test_xss_in_analyst_note_is_escaped(self):
        """Du HTML injecté dans une note analyste est échappé."""
        AnalystNote.objects.create(
            application=self.application,
            analyst=self.analyst_user,
            comment='<img src=x onerror=alert(1)>'
        )
        self.client.login(username='client@test.com', password='testpass123')
        response = self.client.get(reverse('messages'))
        self.assertNotContains(response, '<img src=x onerror=alert(1)>')

    # --- Access Control ---

    def test_client_cannot_view_other_users_application_detail(self):
        """Un client ne peut pas accéder aux détails d'une demande d'un autre client via le portail analyste."""
        self.client.login(username='client@test.com', password='testpass123')
        response = self.client.get(
            reverse('analyst_application_detail', args=[self.application.id])
        )
        self.assertRedirects(response, reverse('login'))

    def test_anonymous_cannot_access_profile(self):
        """Un utilisateur non connecté ne peut pas accéder au profil."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_cannot_delete_account(self):
        """Un utilisateur non connecté ne peut pas supprimer de compte."""
        response = self.client.post(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='client@test.com').exists())

    def test_analyst_update_status_requires_staff(self):
        """Un utilisateur non-staff ne peut pas modifier le statut d'une demande."""
        self.client.login(username='client@test.com', password='testpass123')
        response = self.client.post(
            reverse('analyst_update_status', args=[self.application.id]),
            data=json.dumps({'status': 'Approved'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
        self.application.refresh_from_db()
        self.assertIsNone(self.application.final_decision)

    # --- Security Headers ---

    def test_clickjacking_protection_header(self):
        """Le header X-Frame-Options est présent dans les réponses."""
        response = self.client.get(reverse('login'))
        self.assertIn(response.headers.get('X-Frame-Options', '').upper(), ['DENY', 'SAMEORIGIN'])

    def test_content_type_nosniff_header(self):
        """Le header X-Content-Type-Options est présent."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.headers.get('X-Content-Type-Options', ''), 'nosniff')

    # --- API Security ---

    def test_api_rejects_invalid_json(self):
        """L'API rejette un body JSON invalide."""
        response = self.client.post(
            reverse('api_predict'),
            data='not json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_api_rejects_negative_age(self):
        """L'API rejette un âge négatif."""
        data = VALID_API_DATA.copy()
        data['age'] = -5
        response = self.client.post(
            reverse('api_predict'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_api_rejects_age_over_limit(self):
        """L'API rejette un âge supérieur à 80."""
        data = VALID_API_DATA.copy()
        data['age'] = 150
        response = self.client.post(
            reverse('api_predict'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


# ============================================================
# 12. TESTS DE PERFORMANCE
# ============================================================

import time


class PerformanceTests(TestCase):
    """Mesure les temps de réponse des endpoints principaux (<500ms)."""

    MAX_RESPONSE_MS = 500

    def setUp(self):
        self.client_user = create_client_user()
        self.analyst_user = create_analyst_user()
        self.application = create_application(self.client_user)

    def _assert_fast(self, url, method='get', login_as=None, data=None, content_type=None):
        if login_as:
            self.client.login(username=login_as, password='testpass123')
        start = time.time()
        if method == 'post':
            kwargs = {'data': data}
            if content_type:
                kwargs['content_type'] = content_type
            response = self.client.post(url, **kwargs)
        else:
            response = self.client.get(url)
        elapsed_ms = (time.time() - start) * 1000
        self.assertLess(elapsed_ms, self.MAX_RESPONSE_MS,
            f"{url} took {elapsed_ms:.0f}ms (limit: {self.MAX_RESPONSE_MS}ms)")
        return response, elapsed_ms

    def test_login_page_performance(self):
        """La page de login répond en moins de 500ms."""
        _, ms = self._assert_fast(reverse('login'))

    def test_register_page_performance(self):
        """La page d'inscription répond en moins de 500ms."""
        _, ms = self._assert_fast(reverse('register'))

    def test_dashboard_performance(self):
        """Le dashboard client répond en moins de 500ms."""
        _, ms = self._assert_fast(reverse('dashboard'), login_as='client@test.com')

    def test_profile_performance(self):
        """La page profil répond en moins de 500ms."""
        _, ms = self._assert_fast(reverse('profile'), login_as='client@test.com')

    def test_messages_performance(self):
        """La page messages répond en moins de 500ms."""
        _, ms = self._assert_fast(reverse('messages'), login_as='client@test.com')

    def test_analyst_dashboard_performance(self):
        """Le dashboard analyste répond en moins de 500ms."""
        _, ms = self._assert_fast(reverse('analyst_dashboard'), login_as='analyst@test.com')

    def test_analyst_detail_performance(self):
        """Le détail d'une application (analyste) répond en moins de 500ms."""
        _, ms = self._assert_fast(
            reverse('analyst_application_detail', args=[self.application.id]),
            login_as='analyst@test.com'
        )

    def test_api_predict_performance(self):
        """L'API de prédiction répond en moins de 500ms."""
        _, ms = self._assert_fast(
            reverse('api_predict'), method='post',
            data=VALID_API_DATA, content_type='application/json'
        )

    def test_legal_page_performance(self):
        """La page mentions légales répond en moins de 500ms."""
        _, ms = self._assert_fast(reverse('legal'))
