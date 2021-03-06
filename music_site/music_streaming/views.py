from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection

from genres.models import Genre
from artists.models import Artist
from tracks.models import Track
from albums.models import Album
from playlists.models import Playlist
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

# Create your views here.

def index(request):
    return redirect('login')

def createuser(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = User.objects.create_user(
            username = username,
            email = email,
            password = password
        )
        print("USER CREADO")
    except:
        print("ERROR")
        raise Http404("ERROR WHILE CREATING USER")
    return redirect('login')


@login_required
def home(request):
    user = request.user
    genres = Genre.objects.all()
    artists = Artist.objects.all()
    tracks = Track.objects.all()
    albums = Album.objects.all()
    playlists = Playlist.objects.all()
    misCanciones = custom_sql_dictfetchall(
        """
        SELECT DISTINCT track.*
        FROM userTrack
	        JOIN track on userTrack.trackid = track.id
        WHERE usertrack.userid = {id}

        UNION 

        SELECT track.*
        FROM customer
            JOIN auth_user on customer.user_id = auth_user.id
            JOIN invoice on invoice.customerid  = customer.id
            JOIN invoiceline on invoice.id = invoiceline.invoiceid
            JOIN track on invoiceline.trackid = track.id 
        WHERE auth_user.id = {id}
        """.format(id=user.id)
    )
    return render(
        request, 
        'home.html', 
        {
            'user': user,
            'genres': genres,
            'artists': artists,
            'tracks': tracks,
            'albums': albums,
            "playlists": playlists,
            "misCanciones": misCanciones
        }
    )

def search(request):
    user = request.user
    search = request.POST.get('search')
    resultSearch = custom_sql_dictfetchall(
        """
        select id, tipo, name from (
            select id as id, 'artist' as tipo, name as name from artist a
            union
            select genreid as id, 'genre' as tipo, name as name from genre g
            union
            select id as id, 'album' as tipo, title as name from album a
            union
            select id as id, 'track' as tipo, name as name from track t where t.active = TRUE
        ) as global
        where LOWER(name) LIKE LOWER('%{search}%');
        """.format(search=search)
    )
    return render(
        request, 
        'search.html',
        {
            'user': user,
            'resultSearch': resultSearch
        }
    )

@login_required
def admin_users(request):
    user = request.user
    users = User.objects.all()
    groups = Group.objects.all()
    userGroups = {}
    for usuario in users:
        if (len(usuario.groups.all()) > 0):
            userGroups[usuario.username] = usuario.groups.all()[0].name
    print(userGroups)

    return render(
        request,
        'admin_users.html',
        {
            'user': user,
            'users': users,
            'groups': groups,
            'userGroups': userGroups
        }
    )

@login_required
def admin_users_update_object(request, id):
    try:
        superuser = True if request.POST.get('superuser') else False
        active = True if request.POST.get('active') else False
        selectedGroup = request.POST.get('selectedGroup')
        usuario = User.objects.get(pk = id)
        usuario.is_superuser = superuser
        usuario.is_active = active
        usuario.save()
        if selectedGroup != "None":
            group = Group.objects.get(name = selectedGroup)
            usuario.groups.clear()
            usuario.groups.add(group)
        else:
            usuario.groups.clear()

    except User.DoesNotExist:
        raise Http404("User does not exist")
    return redirect('admin')

@login_required
def admin_groups(request):
    user = request.user
    groups = Group.objects.all()
    createPermission = Permission.objects.get(codename = 'add_track')
    readPermission = Permission.objects.get(codename = 'view_track')
    updatePermission = Permission.objects.get(codename = 'change_track')
    deletePermission = Permission.objects.get(codename = 'delete_track')
    return render(
        request,
        'admin_groups.html', 
        {
            'user': user,
            'groups': groups,
            'createPermission': createPermission,
            'readPermission': readPermission,
            'updatePermission': updatePermission,
            'deletePermission': deletePermission
        }
    )

@login_required
def admin_groups_create_new(request):
    user = request.user
    name = request.POST.get('name')
    createPermission = True if request.POST.get('createPermission') else False
    readPermission = True if request.POST.get('readPermission') else False
    updatePermission = True if request.POST.get('updatePermission') else False
    deletePermission = True if request.POST.get('deletePermission') else False
    group = Group.objects.create(name = name)
    group.save()

    if createPermission:
        addCreatePermissions(group)
    if readPermission:
        addReadPermissions(group)
    if updatePermission:
        addUpdatePermissions(group)
    if deletePermission:
        addDeletePermissions(group)

    return redirect('admin_groups')

@login_required
def admin_groups_update_object(request, id):
    try:
        name = request.POST.get('name')
        createPermissions = request.POST.get('createPermissions')
        readPermissions = request.POST.get('readPermissions')
        updatePermissions = request.POST.get('updatePermissions')
        deletePermissions = request.POST.get('deletePermissions')
        group = Group.objects.get(pk = id)
        group.name = name
        group.permissions.clear()
        group.save()
        
        if createPermissions:
            addCreatePermissions(group)
        if readPermissions:
            addReadPermissions(group)
        if updatePermissions:
            addUpdatePermissions(group)
        if deletePermissions:
            addDeletePermissions(group)
            
    except Group.DoesNotExist:
        raise Http404("Group does not exist")
    return redirect('admin_groups')

@login_required
def admin_groups_delete(request, id):
    try:
        group = Group.objects.get(pk = id)
        group.delete()
    except Group.DoesNotExist:
        raise Http404("Group does not exist")
    return redirect('admin_groups')

@login_required
def admin_permissions(request):
    user = request.user
    permissions = Permission.objects.all()
    return render(
        request,
        'admin_permissions.html', 
        {
            'user': user,
            'permissions': permissions
        }
    )

def custom_sql_fetchOne(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchone()
    return data

def custom_sql_fetchAll(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    return data

def custom_sql_dictfetchall(query):
    "Return all rows from a cursor as a dict"
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

def print_query(data):
    for item in data:
        print(item)


def addCreatePermissions(group):
    # Permissions Create
    # add_logentry = Permission.objects.get(codename = 'add_logentry')
    # add_permission = Permission.objects.get(codename = 'add_permission')
    # add_user = Permission.objects.get(codename = 'add_user')
    # add_contenttype = Permission.objects.get(codename = 'add_contenttype')
    # add_session = Permission.objects.get(codename = 'add_session')
    add_group = Permission.objects.get(codename = 'add_group')
    add_album = Permission.objects.get(codename = 'add_album')
    add_artist = Permission.objects.get(codename = 'add_artist')
    add_customer = Permission.objects.get(codename = 'add_customer')
    add_employee = Permission.objects.get(codename = 'add_employee')
    add_genre = Permission.objects.get(codename = 'add_genre')
    add_invoiceline = Permission.objects.get(codename = 'add_invoiceline')
    add_invoice = Permission.objects.get(codename = 'add_invoice')
    add_mediatype = Permission.objects.get(codename = 'add_mediatype')
    add_playlist = Permission.objects.get(codename = 'add_playlist')
    add_playlisttrack = Permission.objects.get(codename = 'add_playlisttrack')
    add_track = Permission.objects.get(codename = 'add_track')
    add_useralbum = Permission.objects.get(codename = 'add_useralbum')
    add_userartist = Permission.objects.get(codename = 'add_userartist')
    add_usergenre = Permission.objects.get(codename = 'add_usergenre')
    add_userplaylist = Permission.objects.get(codename = 'add_userplaylist')
    add_usertrack = Permission.objects.get(codename = 'add_usertrack')

    group.permissions.add(
        add_group,
        add_album,
        add_artist,
        add_customer,
        add_employee,
        add_genre,
        add_invoiceline,
        add_invoice,
        add_mediatype,
        add_playlist,
        add_playlisttrack,
        add_track,
        add_useralbum,
        add_userartist,
        add_usergenre,
        add_userplaylist,
        add_usertrack
    )

def addReadPermissions(group):
    # Permissions Read
    # view_logentry = Permission.objects.get(codename = 'view_logentry')
    # view_contenttype = Permission.objects.get(codename = 'view_contenttype')
    # view_session = Permission.objects.get(codename = 'view_session')
    view_permission = Permission.objects.get(codename = 'view_permission')
    view_group = Permission.objects.get(codename = 'view_group')
    view_user = Permission.objects.get(codename = 'view_user')
    view_album = Permission.objects.get(codename = 'view_album')
    view_artist = Permission.objects.get(codename = 'view_artist')
    view_customer = Permission.objects.get(codename = 'view_customer')
    view_employee = Permission.objects.get(codename = 'view_employee')
    view_genre = Permission.objects.get(codename = 'view_genre')
    view_invoiceline = Permission.objects.get(codename = 'view_invoiceline')
    view_invoice = Permission.objects.get(codename = 'view_invoice')
    view_mediatype = Permission.objects.get(codename = 'view_mediatype')
    view_playlist = Permission.objects.get(codename = 'view_playlist')
    view_playlisttrack = Permission.objects.get(codename = 'view_playlisttrack')
    view_track = Permission.objects.get(codename = 'view_track')
    view_useralbum = Permission.objects.get(codename = 'view_useralbum')
    view_userartist = Permission.objects.get(codename = 'view_userartist')
    view_usergenre = Permission.objects.get(codename = 'view_usergenre')
    view_userplaylist = Permission.objects.get(codename = 'view_userplaylist')
    view_usertrack = Permission.objects.get(codename = 'view_usertrack')

    group.permissions.add(
        view_permission,
        view_group,
        view_user,
        view_album,
        view_artist,
        view_customer,
        view_employee,
        view_genre,
        view_invoiceline,
        view_invoice,
        view_mediatype,
        view_playlist,
        view_playlisttrack,
        view_track,
        view_useralbum,
        view_userartist,
        view_usergenre,
        view_userplaylist,
        view_usertrack
    )

def addUpdatePermissions(group):
    # Permissions Update
    # change_logentry = Permission.objects.get(codename = 'change_logentry')
    # change_permission = Permission.objects.get(codename = 'change_permission')
    # change_contenttype = Permission.objects.get(codename = 'change_contenttype')
    # change_session = Permission.objects.get(codename = 'change_session')
    change_group = Permission.objects.get(codename = 'change_group')
    change_user = Permission.objects.get(codename = 'change_user')
    change_album = Permission.objects.get(codename = 'change_album')
    change_artist = Permission.objects.get(codename = 'change_artist')
    change_customer = Permission.objects.get(codename = 'change_customer')
    change_employee = Permission.objects.get(codename = 'change_employee')
    change_genre = Permission.objects.get(codename = 'change_genre')
    change_invoiceline = Permission.objects.get(codename = 'change_invoiceline')
    change_invoice = Permission.objects.get(codename = 'change_invoice')
    change_mediatype = Permission.objects.get(codename = 'change_mediatype')
    change_playlist = Permission.objects.get(codename = 'change_playlist')
    change_playlisttrack = Permission.objects.get(codename = 'change_playlisttrack')
    change_track = Permission.objects.get(codename = 'change_track')
    change_useralbum = Permission.objects.get(codename = 'change_useralbum')
    change_userartist = Permission.objects.get(codename = 'change_userartist')
    change_usergenre = Permission.objects.get(codename = 'change_usergenre')
    change_userplaylist = Permission.objects.get(codename = 'change_userplaylist')
    change_usertrack = Permission.objects.get(codename = 'change_usertrack')

    group.permissions.add(
        change_group,
        change_user,
        change_album,
        change_artist,
        change_customer,
        change_employee,
        change_genre,
        change_invoiceline,
        change_invoice,
        change_mediatype,
        change_playlist,
        change_playlisttrack,
        change_track,
        change_useralbum,
        change_userartist,
        change_usergenre,
        change_userplaylist,
        change_usertrack
    )

def addDeletePermissions(group):
    # Permissions Delete
    # delete_logentry = Permission.objects.get(codename = 'delete_logentry')
    # delete_permission = Permission.objects.get(codename = 'delete_permission')
    # delete_user = Permission.objects.get(codename = 'delete_user')
    # delete_contenttype = Permission.objects.get(codename = 'delete_contenttype')
    # delete_session = Permission.objects.get(codename = 'delete_session')
    delete_group = Permission.objects.get(codename = 'delete_group')
    delete_album = Permission.objects.get(codename = 'delete_album')
    delete_artist = Permission.objects.get(codename = 'delete_artist')
    delete_customer = Permission.objects.get(codename = 'delete_customer')
    delete_employee = Permission.objects.get(codename = 'delete_employee')
    delete_genre = Permission.objects.get(codename = 'delete_genre')
    delete_invoiceline = Permission.objects.get(codename = 'delete_invoiceline')
    delete_invoice = Permission.objects.get(codename = 'delete_invoice')
    delete_mediatype = Permission.objects.get(codename = 'delete_mediatype')
    delete_playlist = Permission.objects.get(codename = 'delete_playlist')
    delete_playlisttrack = Permission.objects.get(codename = 'delete_playlisttrack')
    delete_track = Permission.objects.get(codename = 'delete_track')
    delete_useralbum = Permission.objects.get(codename = 'delete_useralbum')
    delete_userartist = Permission.objects.get(codename = 'delete_userartist')
    delete_usergenre = Permission.objects.get(codename = 'delete_usergenre')
    delete_userplaylist = Permission.objects.get(codename = 'delete_userplaylist')
    delete_usertrack = Permission.objects.get(codename = 'delete_usertrack')

    group.permissions.add(
        delete_group,
        delete_album,
        delete_artist,
        delete_customer,
        delete_employee,
        delete_genre,
        delete_invoiceline,
        delete_invoice,
        delete_mediatype,
        delete_playlist,
        delete_playlisttrack,
        delete_track,
        delete_useralbum,
        delete_userartist,
        delete_usergenre,
        delete_userplaylist,
        delete_usertrack
    )