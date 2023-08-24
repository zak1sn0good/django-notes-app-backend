from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@api_view(["GET"])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting note'
        },
    ]
    return Response(routes, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getNotes(request):
    notes = Note.objects.all().filter(owner=request.user.id)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getSingleNote(request, id):
    try:
        note = Note.objects.get(id=id)
    except Note.DoesNotExist:
        return Response("this note doesn't exist!", status=status.HTTP_404_NOT_FOUND)
    if note.owner and note.owner.pk == request.user.id:
        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        raise PermissionDenied()
    
        
        

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def updateNote(request, id):
    data = request.data
    try:
        note = Note.objects.get(id=id)
    except Note.DoesNotExist:
        return Response("this note doesn't exist!!", status=status.HTTP_404_NOT_FOUND)
    if note.owner and note.owner.pk == request.user.id:
        serializer = NoteSerializer(instance=note, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("provided data is invalid", status=status.HTTP_400_BAD_REQUEST)
    else:
        raise PermissionDenied()         
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteNote(request, id):
    try:
        note = Note.objects.get(id=id)
    except Note.DoesNotExist:
        return Response(f"note with id: {id} doesn't exist", status=status.HTTP_404_NOT_FOUND)
    if note.owner != None and note.owner.pk == request.user.id:
        note.delete()
        return Response(f"note with id: {id} successfully deleted!", status=status.HTTP_200_OK)
    else:
        raise PermissionDenied()
    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createNote(request):
    try:
        data = request.data
        note = Note.objects.create(body=data["body"], owner=request.user)
        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)    
    except:
        return Response("invalid or missing inputs", status=status.HTTP_400_BAD_REQUEST)

