import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime


Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True)  # ID único de usuario
    nombre_usuario = Column(String(50), unique=True, nullable=False)  # Nombre de usuario único
    nombre_completo = Column(String(100), nullable=False)  # Nombre completo del usuario
    correo = Column(String(100), unique=True, nullable=False)  # Correo electrónico único del usuario
    contraseña = Column(String(100), nullable=False)  # Contraseña del usuario
    fecha_creacion = Column(DateTime, default=datetime.now)  # Fecha de creación de la cuenta

    # Relación uno a muchos con Publicación
    publicaciones = relationship('Publicacion', back_populates='usuario')  # Relación con las publicaciones del usuario
    # Relación muchos a muchos con Seguidor
    seguidores = relationship('Seguidor', back_populates='usuario')  # Relación con los seguidores del usuario
    seguidos = relationship('Seguidor', back_populates='seguido')  # Relación con los usuarios seguidos por el usuario

class Seguidor(Base):
    __tablename__ = 'seguidor'  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True)  # ID único de la relación de seguimiento
    seguidor_id = Column(Integer, ForeignKey('usuario.id'))  # ID del seguidor
    seguido_id = Column(Integer, ForeignKey('usuario.id'))  # ID del usuario seguido

    # Relación muchos a uno con Usuario (seguidor)
    usuario = relationship('Usuario', back_populates='seguidores', foreign_keys=[seguidor_id])
    # Relación muchos a uno con Usuario (seguido)
    seguido = relationship('Usuario', back_populates='seguidos', foreign_keys=[seguido_id])

class Publicacion(Base):
    __tablename__ = 'publicacion'  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True)  # ID único de la publicación
    usuario_id = Column(Integer, ForeignKey('usuario.id'))  # ID del usuario que realizó la publicación
    texto = Column(String(300))  # Texto de la publicación
    fecha_publicacion = Column(DateTime, default=datetime.now)  # Fecha de publicación de la publicación

    # Relación muchos a uno con Usuario
    usuario = relationship('Usuario', back_populates='publicaciones')  # Relación con el usuario que realizó la publicación
    # Relación uno a muchos con Multimedia
    multimedia = relationship('Multimedia', back_populates='publicacion')  # Relación con los archivos multimedia de la publicación
    # Relación uno a muchos con Comentario
    comentarios = relationship('Comentario', back_populates='publicacion')  # Relación con los comentarios de la publicación

class Multimedia(Base):
    __tablename__ = 'multimedia'  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True)  # ID único del archivo multimedia
    publicacion_id = Column(Integer, ForeignKey('publicacion.id'))  # ID de la publicación asociada al archivo multimedia
    url = Column(String(200))  # URL del archivo multimedia

    # Relación muchos a uno con Publicación
    publicacion = relationship('Publicacion', back_populates='multimedia')  # Relación con la publicación asociada

class Comentario(Base):
    __tablename__ = 'comentario'  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True)  # ID único del comentario
    publicacion_id = Column(Integer, ForeignKey('publicacion.id'))  # ID de la publicación a la que se refiere el comentario
    usuario_id = Column(Integer, ForeignKey('usuario.id'))  # ID del usuario que realizó el comentario
    texto = Column(String(300))  # Texto del comentario
    fecha_comentario = Column(DateTime, default=datetime.now)  # Fecha de creación del comentario

    # Relación muchos a uno con Publicación
    publicacion = relationship('Publicacion', back_populates='comentarios')  # Relación con la publicación a la que se refiere el comentario
    # Relación muchos a uno con Usuario
    usuario = relationship('Usuario')  # Relación con el usuario que realizó el comentario
    
    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
