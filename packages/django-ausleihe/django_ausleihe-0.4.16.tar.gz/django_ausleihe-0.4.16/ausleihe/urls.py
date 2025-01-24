# vim: set tw=140:

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'ausleihe'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('medien', views.MediumList.as_view(), name='medium-list'),
    path('medien/<str:medium_id>', views.MediumDetail.as_view(), name='medium-detail'),
    path('bücher', views.BuchList.as_view(), name='buch-list'),
    path('bücher/neu', views.BuchCreate.as_view(), name='buch-create'),
    path('bücher/<int:buch_id>', views.BuchDetail.as_view(), name='buch-detail'),
    path('bücher/<int:buch_id>/bearbeiten', views.BuchEdit.as_view(), name='buch-edit'),
    path('autoren', views.AutorList.as_view(), name='autor-list'),
    path('autoren/neu', views.AutorCreate.as_view(), name='autor-create'),
    path('autoren/<int:autor_id>/bearbeiten', views.AutorEdit.as_view(), name='autor-edit'),
    path('autoren/<int:autor_id>', views.AutorDetail.as_view(), name='autor-detail'),
    path('verlage', views.VerlagList.as_view(), name='verlag-list'),
    path('verlage/neu', views.VerlagCreate.as_view(), name='verlag-create'),
    path('verlage/<int:verlag_id>', views.VerlagDetail.as_view(), name='verlag-detail'),
    path('verlage/<int:verlag_id>/bearbeiten', views.VerlagEdit.as_view(), name='verlag-edit'),
    path('skills', views.SkillList.as_view(), name='skill-list'),
    path('skill/neu', views.SkillCreate.as_view(), name='skill-create'),
    path('skill/<int:skill_id>', views.SkillDetail.as_view(), name='skill-detail'),
    path('skill/<int:skill_id>/bearbeiten', views.SkillEdit.as_view(), name='skill-edit'),
    path('skill/<int:skill_id>/reservieren', views.SkillReserve.as_view(), name='skill-reserve'),
    path('skill/<int:skill_id>/reservieren/<int:v_id>', views.SkillVerfuegbarkeitReserve.as_view(), name='skill-verfuegbarkeit-reserve'),
    path('skillsets', views.SkillsetList.as_view(), name='skillset-list'),
    path('skillset/<int:skillset_id>', views.SkillsetDetail.as_view(), name='skillset-detail'),
    path('skillset/<int:skillset_id>/bearbeiten', views.SkillsetEdit.as_view(), name='skillset-edit'),
    path('skillset/<int:skillset_id>/duplizieren', views.SkillsetDuplicate.as_view(), name='skillset-duplicate'),
    path('skillsets/neu', views.SkillsetCreate.as_view(), name='skillset-create'),
    path('skillsetitems', views.SkillsetItemList.as_view(), name='skillsetitem-list'),
    path('skillsetitems/neu', views.SkillsetItemCreate.as_view(), name='skillsetitem-create'),
    path('skillsetitems/<int:skillsetitem_id>/bearbeiten', views.SkillsetItemEdit.as_view(), name='skillsetitem-edit'),
    path('skillsetitems/<int:skillsetitem_id>/loeschen', views.SkillsetItemDelete.as_view(), name='skillsetitem-delete'),
    path('gebäude', views.GebaeudeList.as_view(), name='gebaeude-list'),
    path('gebäude/neu', views.GebaeudeCreate.as_view(), name='gebaeude-create'),
    path('gebäude/<int:gebaeude_id>/bearbeiten', views.GebaeudeEdit.as_view(), name='gebaeude-edit'),
    path('räume', views.RaumList.as_view(), name='raum-list'),
    path('raum/neu', views.RaumCreate.as_view(), name='raum-create'),
    path('raum/<int:raum_id>/bearbeiten', views.RaumEdit.as_view(), name='raum-edit'),
    path('raum/importieren', views.RaumImport.as_view(), name='raum-import'),
    path('verleihen', views.Verleihen.as_view(), name='verleihen'),
    path('verliehen', views.LeiheList.as_view(), name='verliehen'),
    path('verliehen/suche', views.LeiheUserSuche.as_view(), name='verliehen-an-suche'),
    path('verliehen/an', views.LeiheUserDetail.as_view(), name='verliehen-an'),
    path('zeiten', views.VerfuegbarkeitCreate.as_view(), name='verfuegbarkeit-create'),
    path('zeit/<int:v_id>/bearbeiten', views.VerfuegbarkeitUpdate.as_view(), name='verfuegbarkeit-edit'),
    path('zeit/<int:v_id>/loeschen', views.VerfuegbarkeitDelete.as_view(), name='verfuegbarkeit-delete'),
    path('zuruecknehmen/<int:leihe_id>', views.Zuruecknehmen.as_view(), name='zuruecknehmen'),
    path('reservierungen', views.ReservierungList.as_view(), name='reservierung-list'),
    path('reservierung/<int:reservierung_id>', views.ReservierungDetail.as_view(), name='reservierung-detail'),
    path('reservierung/<int:reservierung_id>/stornieren', views.ReservierungDelete.as_view(), name='reservierung-delete'),
    path('reservierung/<int:reservierung_id>/verleihen', views.ReservierungVerleihen.as_view(), name='reservierung-verleihen'),
    path('nutzungsordnungen', views.NutzungsordnungList.as_view(), name='nutzungsordnung-list'),
    path('nutzungsordnung/akzeptieren', views.AkzeptiereNutzungsordnung.as_view(), name='nutzungsordnung-akzeptieren'),
    path('nutzungsordnung/neu', views.NutzungsordnungCreate.as_view(), name='nutzungsordnung-create'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
