from django.views import View
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import VerificationRequest, Verification, RequestType, Card
from .forms import DocumentUploadForm


class VerificationView(LoginRequiredMixin, View):
    def get(self, request):
        upload_forms, upload_card_forms, pending_table, approved_table, decline_table, exclude_verifications, exclude_card_verifications = [], [], [], [], [], [], {'CARD_FRONT': [], 'CARD_BACK': []}
        verification_requests = VerificationRequest.objects.filter(user=request.user)
        for vr in verification_requests:
            if vr.status_id == 1:
                approved_table.append({
                    'type': _(vr.type.name),
                    'old_file_name': vr.old_file_name,
                    'status': _(f'STATUS_{vr.status.name}'),
                    'created_at': vr.created_at,
                    'comment': vr.comment,
                })
                exclude_verifications.append(vr.type.name)
                if vr.card and vr.type_id in [1, 2, ]:
                    exclude_card_verifications[vr.type.name].append(vr.card_id)
            if vr.status_id == 2:
                pending_table.append({
                    'type': _(vr.type.name),
                    'old_file_name': vr.old_file_name,
                    'status': _(f'STATUS_{vr.status.name}'),
                    'created_at': vr.created_at,
                    'comment': vr.comment,
                })
                exclude_verifications.append(vr.type.name)
                if vr.card and vr.type_id in [1, 2, ]:
                    exclude_card_verifications[vr.type.name].append(vr.card_id)
            if vr.status_id == 3:
                decline_table.append({
                    'type': _(vr.type.name),
                    'old_file_name': vr.old_file_name,
                    'status': _(f'STATUS_{vr.status.name}'),
                    'created_at': vr.created_at,
                    'comment': vr.comment,
                })
        v = Verification.objects.get(user=request.user)
        cards = Card.objects.filter(user=request.user)
        if not len(cards):
            exclude_verifications.append('DD')
        request_types = RequestType.objects.filter(enabled=True)
        for rt in request_types:
            if rt.name == 'DD' and rt.name not in exclude_verifications:
                if not v.declaration:
                    upload_forms.append({
                        'id': rt.id,
                        'type': _(rt.name),
                        'status': _('STATUS_OPEN'),
                        'description': rt.description,
                    })
            if rt.name == 'ID' and rt.name not in exclude_verifications:
                if not v.identification:
                    upload_forms.append({
                        'id': rt.id,
                        'type': _(rt.name),
                        'status': _('STATUS_OPEN'),
                        'description': rt.description,
                    })
            if rt.name == 'INVOICE' and rt.name not in exclude_verifications:
                if not v.invoice:
                    upload_forms.append({
                        'id': rt.id,
                        'type': _(rt.name),
                        'status': _('STATUS_OPEN'),
                        'description': rt.description,
                    })
            if rt.name == 'OTHER':
                upload_forms.append({
                    'id': rt.id,
                    'type': _(rt.name),
                    'status': _('STATUS_OPEN'),
                    'description': rt.description,
                })
            if rt.name in ['CARD_FRONT', 'CARD_BACK', ]:
                for c in cards:
                    if not c.is_verified and c.id not in exclude_card_verifications[rt.name]:
                        upload_card_forms.append({
                            'id': rt.id,
                            'type': _(rt.name),
                            'card_id': c.id,
                            'card_number': c.number,
                            'status': _('STATUS_OPEN'),
                            'description': rt.description,
                        })
        context = {
            'nav_verification': 'active',
            'nav_profile_collapsed': 'show',
            'title_category': _('VERIFICATION_PAGE_TITLE'),
            'upload_card_forms': upload_card_forms,
            'pending_table': pending_table,
            'approved_table': approved_table,
            'declined_table': decline_table,
        }
        if len(upload_forms):
            context['upload_forms'] = upload_forms
        return render(request, 'verification/index.html', context=context)

    def post(self, request):
        if len(request.FILES) > 1:
            messages.add_message(request, messages.ERROR, _('VERIFICATION_UPLOAD_ERROR_MANYFILES'))
            return redirect('verification')

        file = request.FILES.get('file', None)
        if file is not None:
            form = DocumentUploadForm(
                data={
                    'old_file_name': file.name,
                    'type': request.POST.get('type', None),
                    'status': 2,
                    'user': request.user,
                    'card': request.POST.get('card_id', None),
                },
                files=request.FILES,
            )
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, _('VERIFICATION_REQUEST_SUCCESSFULLY_CREATED'))
                return redirect('verification')
            for field in form:
                for error in field.errors:
                    messages.add_message(request, messages.ERROR, error)
            return redirect('verification')

        messages.add_message(request, messages.ERROR, _('VERIFICATION_UPLOAD_ERROR_NOFILE'))
        return redirect('verification')
