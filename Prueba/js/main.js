import { GestorPedidos } from './gestorPedidos.js';
import { UI } from './ui.js';

const elementos = {
  form: document.getElementById('formPedido'),
  inputPedido: document.getElementById('inputPedido'),
  filtroEstado: document.getElementById('filtroEstado'),
  tablaPedidos: document.getElementById('tablaPedidos'),
  totalPedidos: document.getElementById('totalPedidos'),
  countPendientes: document.getElementById('countPendientes'),
  countPreparacion: document.getElementById('countPreparacion'),
  countListos: document.getElementById('countListos'),
  resumenPendientes: document.getElementById('resumenPendientes'),
  resumenPreparacion: document.getElementById('resumenPreparacion'),
  resumenListos: document.getElementById('resumenListos'),
};

const gestorPedidos = new GestorPedidos();
const ui = new UI(gestorPedidos, elementos);
