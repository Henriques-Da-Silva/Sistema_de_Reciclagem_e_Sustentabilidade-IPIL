from typing import Optional
import datetime
import decimal

from sqlalchemy import DECIMAL, DateTime, ForeignKeyConstraint, Index, Integer, String, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class LocaisColeta(Base):
    __tablename__ = 'locais_coleta'
    __table_args__ = (
        Index('nome', 'nome', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(String(100))
    endereco: Mapped[Optional[str]] = mapped_column(String(100))
    estado: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'1'"))

    locais_coleta_material: Mapped[list['LocaisColetaMaterial']] = relationship('LocaisColetaMaterial', back_populates='locais_coleta')


class Materiais(Base):
    __tablename__ = 'materiais'
    __table_args__ = (
        Index('nome', 'nome', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    pontos: Mapped[decimal.Decimal] = mapped_column(DECIMAL(8, 2), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(String(100))
    dataCadastro: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    locais_coleta_material: Mapped[list['LocaisColetaMaterial']] = relationship('LocaisColetaMaterial', back_populates='materiais')
    coletas: Mapped[list['Coletas']] = relationship('Coletas', back_populates='materiais')


class TipoUsuario(Base):
    __tablename__ = 'tipo_usuario'
    __table_args__ = (
        Index('nome', 'nome', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(String(100))

    usuarios: Mapped[list['Usuarios']] = relationship('Usuarios', back_populates='tipo_usuario')


class LocaisColetaMaterial(Base):
    __tablename__ = 'locais_coleta_material'
    __table_args__ = (
        ForeignKeyConstraint(['idLocalColeta'], ['locais_coleta.id'], name='locais_coleta_material_ibfk_1'),
        ForeignKeyConstraint(['idMaterial'], ['materiais.id'], name='locais_coleta_material_ibfk_2'),
        Index('idLocalColeta', 'idLocalColeta', 'idMaterial', unique=True),
        Index('idMaterial', 'idMaterial')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    idLocalColeta: Mapped[int] = mapped_column(Integer, nullable=False)
    idMaterial: Mapped[int] = mapped_column(Integer, nullable=False)
    dataCadastro: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    locais_coleta: Mapped['LocaisColeta'] = relationship('LocaisColeta', back_populates='locais_coleta_material')
    materiais: Mapped['Materiais'] = relationship('Materiais', back_populates='locais_coleta_material')


class Usuarios(Base):
    __tablename__ = 'usuarios'
    __table_args__ = (
        ForeignKeyConstraint(['idTipoUsuario'], ['tipo_usuario.id'], name='usuarios_ibfk_1'),
        Index('email', 'email', unique=True),
        Index('idTipoUsuario', 'idTipoUsuario')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    idTipoUsuario: Mapped[int] = mapped_column(Integer, nullable=False)
    pontuacao: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    total_reciclado: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False, server_default=text("'0.00'"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    tipo_usuario: Mapped['TipoUsuario'] = relationship('TipoUsuario', back_populates='usuarios')
    coletas: Mapped[list['Coletas']] = relationship('Coletas', back_populates='usuarios')


class Coletas(Base):
    __tablename__ = 'coletas'
    __table_args__ = (
        ForeignKeyConstraint(['idMaterial'], ['materiais.id'], name='coletas_ibfk_2'),
        ForeignKeyConstraint(['idUsuario'], ['usuarios.id'], name='coletas_ibfk_1'),
        Index('idMaterial', 'idMaterial'),
        Index('idUsuario', 'idUsuario')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    idUsuario: Mapped[int] = mapped_column(Integer, nullable=False)
    idMaterial: Mapped[int] = mapped_column(Integer, nullable=False)
    quantidadeKilo: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    pontos_ganhos: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    dataCadastro: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    materiais: Mapped['Materiais'] = relationship('Materiais', back_populates='coletas')
    usuarios: Mapped['Usuarios'] = relationship('Usuarios', back_populates='coletas')