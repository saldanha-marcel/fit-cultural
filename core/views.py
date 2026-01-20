from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import os
import json
from django.core.files.storage import FileSystemStorage
from django.utils.text import get_valid_filename
from .models import TypingTest, TypingTestPhase, BehavioralProfile, TestProgress
from users.models import Users as User

@login_required(login_url='/auth/login')
def index(request):
    # Obter ou criar progresso do usuário
    progress, created = TestProgress.objects.get_or_create(user=request.user)
    
    context = {
        'progress': progress,
    }
    return render(request, 'index.html', context)

@login_required(login_url='/auth/login')
def digitacao(request):
    # Verificar se o usuário já completou o teste de digitação
    progress, created = TestProgress.objects.get_or_create(user=request.user)
    
    if progress.typing_test_completed:
        return render(request, 'core/digitacao_completado.html', {
            'progress': progress,
            'completed_at': progress.typing_test_completed_at
        })
    
    return render(request, 'core/digitacao.html')

@login_required(login_url='/auth/login')
def personalidade(request):
    # Verificar se o usuário completou o teste de digitação
    progress, created = TestProgress.objects.get_or_create(user=request.user)
    
    if progress.behavioral_test_completed:
        print(f"DEBUG: Usuário {request.user.username} já  {progress.behavioral_test_completed_at} completou o teste de personalidade em {progress.behavioral_test_completed_at}")
        return render(request, 'core/personalidade_completado.html', {
            'progress': progress,
            'completed_at': progress.behavioral_test_completed_at
        })
    
    return render(request, 'core/personalidade.html')

@login_required(login_url='/auth/login')
@require_POST
def save_typing_test(request):
    """Salva os resultados do teste de digitação no banco de dados"""
    try:
        data = json.loads(request.body)
        print(f"DEBUG: Dados recebidos: {data}")
        
        # Validar se data é uma lista
        if not isinstance(data, list):
            raise ValueError(f"Esperado lista de fases, recebido: {type(data)}")
        
        if len(data) != 3:
            raise ValueError(f"Esperado 3 fases, recebidas: {len(data)}")
        
        # Calcular médias
        wpm_values = [float(phase['wpm']) for phase in data]
        accuracy_values = [float(phase['accuracy']) for phase in data]
        wpm_average = sum(wpm_values) / len(wpm_values)
        accuracy_average = sum(accuracy_values) / len(accuracy_values)
        
        # Criar teste de digitação
        typing_test = TypingTest.objects.create(
            user=request.user,
            wpm_average=wpm_average,
            accuracy_average=accuracy_average
        )
        
        # Criar fases do teste
        for phase_data in data:
            TypingTestPhase.objects.create(
                typing_test=typing_test,
                phase_number=phase_data['phase'],
                original_phrase=phase_data['originalPhrase'],
                typed_text=phase_data['typedText'],
                time_seconds=float(phase_data['timeSeconds']),
                wpm=float(phase_data['wpm']),
                accuracy=float(phase_data['accuracy'])
            )
        
        # Atualizar progresso do usuário
        progress, created = TestProgress.objects.get_or_create(user=request.user)
        progress.typing_test_completed = True
        progress.typing_test_completed_at = timezone.now()
        progress.save()
        
        print(f"DEBUG: Teste salvo com sucesso para usuário {request.user.username}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Teste salvo com sucesso',
            'test_id': typing_test.id
        })
    except json.JSONDecodeError as e:
        error_msg = f"Erro ao decodificar JSON: {str(e)}"
        print(f"DEBUG: {error_msg}")
        return JsonResponse({
            'status': 'error',
            'message': error_msg
        }, status=400)
    except Exception as e:
        error_msg = f"Erro ao salvar teste: {str(e)}"
        print(f"DEBUG: {error_msg}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'status': 'error',
            'message': error_msg
        }, status=400)

@login_required(login_url='/auth/login')
@require_POST
def save_behavioral_test(request):
    """Salva os resultados do teste de perfil comportamental"""
    try:
        data = json.loads(request.body)
        scores = data.get('scores', {})
        answers = data.get('answers', [])
        
        # Validar scores
        if not all(key in scores for key in ['A', 'B', 'C', 'D', 'dominant']):
            raise ValueError('Scores incompletos')
        
        # Criar perfil comportamental
        behavioral_profile = BehavioralProfile.objects.create(
            user=request.user,
            quadrant_a_score=scores['A'],
            quadrant_b_score=scores['B'],
            quadrant_c_score=scores['C'],
            quadrant_d_score=scores['D'],
            dominant_quadrant=scores['dominant'],
            answers=answers
        )
        
        # Atualizar progresso do usuário
        progress, created = TestProgress.objects.get_or_create(user=request.user)
        progress.behavioral_test_completed = True
        progress.behavioral_test_completed_at = timezone.now()
        progress.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Perfil comportamental salvo com sucesso',
            'profile_id': behavioral_profile.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required(login_url='/auth/login')
def dashboard(request):
    """Renderiza o dashboard do usuário com seus testes e perfis"""
    typing_tests = TypingTest.objects.filter(user=request.user).order_by('-created_at')
    behavioral_profiles = BehavioralProfile.objects.filter(user=request.user).order_by('-created_at')
    progress, created = TestProgress.objects.get_or_create(user=request.user)
    
    context = {
        'typing_tests': typing_tests,
        'behavioral_profiles': behavioral_profiles,
        'progress': progress,
    }
    return render(request, 'core/dashboard.html', context)

@login_required(login_url='/auth/login')
def detalhes_candidato(request, user_id):
    """Renderiza a página de detalhes de um candidato específico"""
    from django.shortcuts import get_object_or_404
    
    # Buscar o usuário pelo ID
    candidato = get_object_or_404(User, id=user_id)
    
    # Buscar último teste de digitação
    typing_test = TypingTest.objects.filter(user=candidato).order_by('-created_at').first()
    
    # Buscar todas as fases do teste de digitação
    typing_phases = []
    if typing_test:
        typing_phases = TypingTestPhase.objects.filter(typing_test=typing_test).order_by('phase_number')
    
    # Buscar último perfil comportamental
    behavioral_profile = BehavioralProfile.objects.filter(user=candidato).order_by('-created_at').first()
    
    # Buscar progresso
    progress = TestProgress.objects.filter(user=candidato).first()
    
    # Calcular tempo total (soma das fases)
    tempo_total_segundos = sum([phase.time_seconds for phase in typing_phases]) if typing_phases else 0
    tempo_total_minutos = int(tempo_total_segundos // 60)
    tempo_total_segundos_resto = int(tempo_total_segundos % 60)
    tempo_total_formatado = f"{tempo_total_minutos:02d}:{tempo_total_segundos_resto:02d}"
    
    context = {
        'candidato': candidato,
        'typing_test': typing_test,
        'typing_phases': typing_phases,
        'behavioral_profile': behavioral_profile,
        'progress': progress,
        'tempo_total': tempo_total_formatado,
    }
    
    return render(request, 'core/detalhes_candidato.html', context)

@login_required(login_url='/auth/login')
def relatorios(request):
    """Renderiza a página de relatórios com dados dos candidatos"""
    from django.db.models import Prefetch
    
    # Buscar todos os usuários que completaram testes
    candidatos = User.objects.filter(
        test_progress__typing_test_completed=True
    ).select_related('test_progress').prefetch_related(
        'typing_tests',
        'behavioral_profiles'
    ).order_by('-test_progress__typing_test_completed_at')
    
    # Preparar dados dos candidatos
    candidatos_data = []
    for user in candidatos:
        # Pegar último teste de digitação
        typing_test = user.typing_tests.order_by('-created_at').first()
        # Pegar último perfil comportamental
        behavioral_profile = user.behavioral_profiles.order_by('-created_at').first()
        
        if typing_test:  # Só incluir se tem teste de digitação
            candidatos_data.append({
                'user': user,
                'typing_test': typing_test,
                'behavioral_profile': behavioral_profile,
                'progress': user.test_progress
            })
    
    context = {
        'candidatos': candidatos_data
    }
    
    return render(request, 'core/listagem_candidatos.html', context)