from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Contact
from .forms import ContactForm


def contact_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        contacts = Contact.objects.filter(
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    else:
        contacts = Contact.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm()

    context = {
        'contacts': contacts,
        'form': form,
        'search_query': search_query,
    }

    return render(
        request,
        'contacts/contact_list.html',
        context
    )


def edit_contact(request, id):
    contact = get_object_or_404(Contact, id=id)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)

        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)

    context = {
        'form': form,
        'contact': contact,
    }

    return render(
        request,
        'contacts/edit_contact.html',
        context
    )


def delete_contact(request, id):
    contact = get_object_or_404(Contact, id=id)

    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')

    context = {
        'contact': contact,
    }

    return render(
        request,
        'contacts/delete_contact.html',
        context
    )