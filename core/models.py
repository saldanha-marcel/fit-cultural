from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TypingTest(models.Model):
    """Modelo para armazenar resultados de testes de digitação"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='typing_tests')
    created_at = models.DateTimeField(auto_now_add=True)
    wpm_average = models.FloatField(help_text="Velocidade média em palavras por minuto")
    accuracy_average = models.FloatField(help_text="Acurácia média em percentual")

    class Meta:
        verbose_name = "Teste de Digitação"
        verbose_name_plural = "Testes de Digitação"
        ordering = ['-created_at']

    def __str__(self):
        return f"Teste de {self.user.get_full_name() or self.user.username} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"


class TypingTestPhase(models.Model):
    """Modelo para armazenar dados de cada fase do teste de digitação"""
    typing_test = models.ForeignKey(TypingTest, on_delete=models.CASCADE, related_name='phases')
    phase_number = models.IntegerField(choices=[(1, 'Fase 1'), (2, 'Fase 2'), (3, 'Fase 3')])
    original_phrase = models.TextField(help_text="Frase original a ser digitada")
    typed_text = models.TextField(help_text="Texto digitado pelo usuário")
    time_seconds = models.FloatField(help_text="Tempo gasto em segundos")
    wpm = models.FloatField(help_text="Velocidade em palavras por minuto")
    accuracy = models.FloatField(help_text="Acurácia em percentual")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fase do Teste de Digitação"
        verbose_name_plural = "Fases dos Testes de Digitação"
        ordering = ['typing_test', 'phase_number']
        unique_together = ['typing_test', 'phase_number']

    def __str__(self):
        return f"Fase {self.phase_number} - Teste {self.typing_test.id}"


class BehavioralProfile(models.Model):
    """Modelo para armazenar resultados do teste de perfil comportamental (Ned Herrmann)"""
    QUADRANT_CHOICES = [
        ('A', 'Pensador Analítico'),
        ('B', 'Pensador Prático'),
        ('C', 'Pensador Relacional'),
        ('D', 'Pensador Inovador'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='behavioral_profiles')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Scores dos 4 quadrantes (0-100)
    quadrant_a_score = models.IntegerField(help_text="Score do Quadrante A - Analítico (Lógico)")
    quadrant_b_score = models.IntegerField(help_text="Score do Quadrante B - Prático (Administrativo)")
    quadrant_c_score = models.IntegerField(help_text="Score do Quadrante C - Relacional (Interpessoal)")
    quadrant_d_score = models.IntegerField(help_text="Score do Quadrante D - Inovador (Criativo)")
    
    # Quadrante dominante
    dominant_quadrant = models.CharField(max_length=1, choices=QUADRANT_CHOICES, help_text="Quadrante com maior score")
    
    # Respostas brutas para referência
    answers = models.JSONField(help_text="Respostas completas do teste")

    class Meta:
        verbose_name = "Perfil Comportamental"
        verbose_name_plural = "Perfis Comportamentais"
        ordering = ['-created_at']

    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username} - {self.dominant_quadrant} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"

    @property
    def scores_dict(self):
        return {
            'A': self.quadrant_a_score,
            'B': self.quadrant_b_score,
            'C': self.quadrant_c_score,
            'D': self.quadrant_d_score,
        }
    
    @property
    def get_dominant_quadrant_display(self):
        return dict(self.QUADRANT_CHOICES).get(self.dominant_quadrant)


class TestProgress(models.Model):
    """Modelo para rastrear o progresso do usuário nos testes"""
    TEST_CHOICES = [
        ('typing', 'Teste de Digitação'),
        ('behavioral', 'Teste de Perfil Comportamental'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='test_progress')
    typing_test_completed = models.BooleanField(default=False, help_text="Teste de digitação completado")
    typing_test_completed_at = models.DateTimeField(null=True, blank=True, help_text="Data de conclusão do teste de digitação")
    
    behavioral_test_completed = models.BooleanField(default=False, help_text="Teste de perfil comportamental completado")
    behavioral_test_completed_at = models.DateTimeField(null=True, blank=True, help_text="Data de conclusão do teste de comportamento")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Progresso do Teste"
        verbose_name_plural = "Progresso dos Testes"

    def __str__(self):
        return f"Progresso de {self.user.get_full_name() or self.user.username}"

    @property
    def all_tests_completed(self):
        return self.typing_test_completed and self.behavioral_test_completed

    @property
    def progress_percentage(self):
        completed = sum([self.typing_test_completed, self.behavioral_test_completed])
        return int((completed / 2) * 100)
