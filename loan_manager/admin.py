from django.contrib import admin
from .models import LoanApplication, AnalystNote

class AnalystNoteInline(admin.TabularInline):
    model = AnalystNote
    extra = 1
    fields = ('analyst', 'comment', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "get_user_name", "marital_status", "income", "risk_score", "risk_flag", "ai_prediction", "final_decision", "created_at")
    list_filter = ("ai_prediction", "final_decision", "risk_flag", "region", "job_category", "created_at")
    search_fields = ("user__username", "user__last_name")
    ordering = ("-created_at",)
    inlines = [AnalystNoteInline]

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_user_name.short_description = "Client"

@admin.register(AnalystNote)
class AnalystNoteAdmin(admin.ModelAdmin):
    list_display = ("application", "analyst", "created_at")
    list_filter = ("analyst",)

"""
get_user_name : Comme ton modèle LoanApplication est lié à User, afficher juste l'ID ne suffit pas pour un analyste. Là, tu vois directement qui est le client.

inlines : C'est le plus important. Quand tu cliques sur une demande de prêt, tu vois tout en bas de la page l'historique des commentaires. Plus besoin de naviguer entre deux tables.

search_fields : Indispensable si tu as beaucoup de données. Tu peux taper le nom d'un client pour retrouver son dossier instantanément.

"""