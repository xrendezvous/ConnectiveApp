from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from calendar import monthcalendar

from .forms import ContactForm, AddressForm
from .models import Contact, Address


@login_required
def main(request, page=1):
    """
    Display the main contacts page with pagination and search functionality.

    Args:
    request (HttpRequest): The request object.
    page (int, optional): The page number for pagination. Defaults to 1.

    Returns:
    HttpResponse: Rendered contacts page.
    """
    contacts = (
        Contact.objects.filter(user=request.user).all().order_by("name")
        if request.user.is_authenticated
        else []
    )
    total_contacts = contacts.count()
    if not contacts:
        error_message = "У вас немає контактів"
    else:
        error_message = None
    query = request.GET.get("q")

    if query:
        contacts = Contact.objects.filter(
            Q(
                address__in=Address.objects.filter(
                    Q(country__icontains=query.strip())
                    | Q(city__icontains=query.strip())
                    | Q(address__icontains=query.strip())
                )
            )
            | Q(name__icontains=query.strip())
            | Q(surname__icontains=query.strip())
            | Q(email__icontains=query.strip())
            | Q(mobile_phone__icontains=query.strip())
            | Q(home_phone__icontains=query.strip())
            | Q(work_phone__icontains=query.strip())
            | Q(birthdate__icontains=query.strip())
        ).distinct()

        if not contacts:
            error_message = "Контактів не знайдено"
        else:
            error_message = None

    per_page = 10
    paginator = Paginator(contacts, per_page)
    page = request.GET.get("page", 1)
    try:
        contacts_on_page = paginator.page(page)
    except PageNotAnInteger:
        contacts_on_page = paginator.page(1)
    except EmptyPage:
        contacts_on_page = paginator.page(paginator.num_pages)

    return render(
        request,
        "app_contacts/contacts.html",
        context={
            "contacts": contacts_on_page,
            "error_message": error_message,
            "total_contacts": total_contacts,
        },
    )


@login_required
def add_contact(request):
    """
    Add a new contact with its address.

    Args:
    request (HttpRequest): The request object.

    Returns:
    HttpResponse: Rendered add contact page.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        form2 = AddressForm(request.POST)

        if form.is_valid() and form2.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact = form.save()

            address = form2.save(commit=False)
            address.contact = contact
            address.save()
            messages.success(
                request,
                f"Контакт '{form.cleaned_data['name']}' {form.cleaned_data['surname']}' додано",
            )
            return redirect(to="app_contacts:contacts")
        else:
            return render(
                request,
                "app_contacts/add_contact.html",
                context={"form": form, "form2": form2},
            )
    return render(
        request,
        "app_contacts/add_contact.html",
        context={"form": ContactForm(), "form2": AddressForm()},
    )


@login_required
def contact_details(request, contact_id):
    """
    Display details of a specific contact.

    Args:
    request (HttpRequest): The request object.
    contact_id (int): The ID of the contact to display.

    Returns:
    HttpResponse: Rendered contact details page.
    """
    a = get_object_or_404(Contact, id=contact_id)
    b = get_object_or_404(Address, contact_id=contact_id)
    return render(
        request,
        "app_contacts/contact_details.html",
        context={"Title": "Контактні дані", "contact": a, "address": b},
    )


@login_required
def delete_contact(request, contact_id):
    """
    Delete a specific contact.

    Args:
    request (HttpRequest): The request object.
    contact_id (int): The ID of the contact to delete.

    Returns:
    HttpResponse: Redirect to the contacts page.
    """
    try:
        a = get_object_or_404(Contact, id=contact_id)
        a.delete()
        messages.success(request, f"Контакт '{a.name} {a.surname}' видалено")
        return redirect(to="app_contacts:contacts")
    except Contact.DoesNotExist:
        raise Http404("Контакт не знайдено")


@login_required
def contact_update(request, contact_id=None):
    """
    Update or add a contact with its address.

    Args:
    request (HttpRequest): The request object.
    contact_id (int, optional): The ID of the contact to update. Defaults to None.

    Returns:
    HttpResponse: Rendered update contact page.
    """
    a = None
    b = None

    if contact_id:
        a = get_object_or_404(Contact, id=contact_id)
        b = get_object_or_404(Address, contact_id=contact_id)

    if request.method == "POST":
        form = ContactForm(request.POST, instance=a)
        form2 = AddressForm(request.POST, instance=b)
        if form.is_valid() and form2.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact = form.save()

            address = form2.save(commit=False)
            address.contact = contact
            address.save()
            if a:
                messages.success(
                    request,
                    f"Контакт '{form.cleaned_data['name']} {form.cleaned_data['surname']}' оновлено",
                )
            else:
                messages.success(
                    request,
                    f"Контакт '{form.cleaned_data['name']} {form.cleaned_data['surname']}' додано",
                )
            return redirect(to="app_contacts:contact_details", contact_id=contact_id)
    else:
        form = ContactForm(
            instance=a,
            initial={"mobile_phone": a.mobile_phone, "birthdate": a.birthdate},
        )
    return render(
        request,
        "app_contacts/contact_update.html",
        context={"form": form, "contact": a, "address": b},
    )


@login_required
def contact_birthday(request):
    """
    Display contacts with birthdays within a specified period.

    Args:
    request (HttpRequest): The request object.

    Returns:
    HttpResponse: Rendered contact birthday page.
    """
    period = request.GET.get("period")

    today = datetime.now()
    current_month = today.month
    current_day = today.day
    passed_this_year = []
    today_birthdays = []
    upcoming_this_month = []

    if period == "today":
        contacts = Contact.objects.filter(
            birthdate__month=current_month,
            birthdate__day=current_day,
            user=request.user,
        )
    elif period == "week":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        current_year = today.year

        contacts = Contact.objects.filter(
            Q(birthdate__year=current_year) &
            Q(birthdate__month=start_date.month) | Q(birthdate__month=end_date.month),
            Q(birthdate__day__gte=start_date.day) & Q(birthdate__day__lte=end_date.day),
            user=request.user,
        )

    elif period == "month":
        passed_this_year = Contact.objects.filter(
            birthdate__month=current_month,
            birthdate__day__lt=current_day,
            user=request.user,
        )
        today_birthdays = Contact.objects.filter(
            birthdate__month=current_month,
            birthdate__day=current_day,
            user=request.user,
        )
        upcoming_this_month = Contact.objects.filter(
            birthdate__month=current_month,
            birthdate__day__gt=current_day,
            user=request.user,
        )
        contacts = []
    else:
        contacts = []

    context = {
        "passed_this_year": passed_this_year,
        "today_birthdays": today_birthdays,
        "upcoming_this_month": upcoming_this_month,
        "period": period,
        "birthday_contacts": contacts,
    }
    return render(request, "app_contacts/contact_birthday.html", context=context)


@login_required
def calendar(request):
    """
    Display a calendar with birthday contacts for a specified month and year.

    Args:
    request (HttpRequest): The request object.

    Returns:
    HttpResponse: Rendered calendar page.
    """
    year = request.GET.get('year')
    month = request.GET.get('month')

    today = datetime.now()
    day_today = today.day

    if month is None or year is None:
        year = today.year
        month = today.month

    month = int(month)
    year = int(year)

    cal_date = monthcalendar(year, month)

    birthday_contacts = Contact.objects.filter(
        user=request.user,
        birthdate__month=month,
        birthdate__year__lte=year
    )
    context = {
        'day_today': day_today,
        'calendar': cal_date,
        'birthday_contacts': birthday_contacts
    }

    return render(request, 'app_contacts/calendar.html', context=context)

