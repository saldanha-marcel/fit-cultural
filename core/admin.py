from django.contrib import admin
from .models import TypingTest, TypingTestPhase, BehavioralProfile, TestProgress

@admin.register(TypingTest)
class TypingTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'wpm_average', 'accuracy_average')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user', 'created_at', 'wpm_average', 'accuracy_average')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(TypingTestPhase)
class TypingTestPhaseAdmin(admin.ModelAdmin):
    list_display = ('typing_test', 'phase_number', 'wpm', 'accuracy', 'time_seconds')
    list_filter = ('phase_number', 'typing_test__created_at')
    search_fields = ('typing_test__user__username',)
    readonly_fields = ('typing_test', 'phase_number', 'original_phrase', 'typed_text', 'time_seconds', 'wpm', 'accuracy', 'created_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(BehavioralProfile)
class BehavioralProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dominant_quadrant', 'created_at', 'quadrant_a_score', 'quadrant_b_score', 'quadrant_c_score', 'quadrant_d_score')
    list_filter = ('dominant_quadrant', 'created_at', 'user')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user', 'created_at', 'quadrant_a_score', 'quadrant_b_score', 'quadrant_c_score', 'quadrant_d_score', 'dominant_quadrant', 'answers')
    
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('user', 'created_at')
        }),
        ('Scores dos Quadrantes', {
            'fields': ('quadrant_a_score', 'quadrant_b_score', 'quadrant_c_score', 'quadrant_d_score', 'dominant_quadrant')
        }),
        ('Respostas Completas', {
            'fields': ('answers',),
            'classes': ('collapse',)
        }),
    )
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(TestProgress)
class TestProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'typing_test_completed', 'behavioral_test_completed', 'progress_percentage')
    list_filter = ('typing_test_completed', 'behavioral_test_completed')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user', 'progress_percentage', 'typing_test_completed_at', 'behavioral_test_completed_at')
    
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('user',)
        }),
        ('Teste de Digitação', {
            'fields': ('typing_test_completed', 'typing_test_completed_at')
        }),
        ('Teste Comportamental', {
            'fields': ('behavioral_test_completed', 'behavioral_test_completed_at')
        }),
        ('Progresso', {
            'fields': ('progress_percentage',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
