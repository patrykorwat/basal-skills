/**
 * Basal Register — Hermes desktop plugin.
 * A small decision tracker pane: propose -> decide (auto review date +30d)
 * -> review outcome, with a one-click markdown export in a simple
 * BASAL-NNN format. Generic tool — it tracks entries you enter here,
 * nothing outside the pane.
 *
 * Install: this file lives at <HERMES_HOME>/desktop-plugins/basal-register/plugin.js
 * Load: "Reload desktop plugins" from the command palette.
 *
 * Plain ESM, loaded uncompiled — UI via jsx() calls, theme classes only.
 */

import { atom, cn, haptic, host, useValue } from '@hermes/plugin-sdk'
import { Fragment, jsx, jsxs } from 'react/jsx-runtime'

const ID = 'basal-register'

// --- state ----------------------------------------------------------------
let storage = null
const entries = atom([])
const draftTitle = atom('')
const draftProposer = atom('')
const decidingId = atom(null)
const decisionDraft = atom('')

const today = () => new Date().toISOString().slice(0, 10)
const plusDays = n => {
  const d = new Date()
  d.setDate(d.getDate() + n)
  return d.toISOString().slice(0, 10)
}

const persist = () => {
  if (storage) storage.set('entries', entries.get())
}

const nextId = list => {
  const max = list.reduce((m, e) => Math.max(m, parseInt(String(e.id).split('-')[1] || '0', 10) || 0), 0)
  return `BASAL-${String(max + 1).padStart(3, '0')}`
}

// --- actions ---------------------------------------------------------------
function propose() {
  const title = draftTitle.get().trim()
  if (!title) {
    host.notify({ kind: 'warning', message: 'Title is required' })
    return
  }
  const list = entries.get()
  const entry = {
    id: nextId(list),
    title,
    date: today(),
    proposer: draftProposer.get().trim(),
    status: 'proposed',
    decision: '',
    consent: '',
    review: '',
    outcome: ''
  }
  entries.set([...list, entry])
  draftTitle.set('')
  draftProposer.set('')
  persist()
  haptic('tap')
}

function startDecide(id) {
  decidingId.set(id)
  decisionDraft.set('')
}

function confirmDecide() {
  const id = decidingId.get()
  const decision = decisionDraft.get().trim()
  if (!decision) {
    host.notify({ kind: 'warning', message: 'Decision text is required' })
    return
  }
  entries.set(entries.get().map(e =>
    e.id === id ? { ...e, status: 'decided', decision, review: plusDays(30) } : e
  ))
  decidingId.set(null)
  persist()
  haptic('tap')
}

function review(id, outcome) {
  entries.set(entries.get().map(e => (e.id === id ? { ...e, outcome } : e)))
  persist()
  haptic('tap')
}

async function copyMarkdown() {
  const md = toMarkdown(entries.get())
  try {
    await navigator.clipboard.writeText(md)
    host.notify({ kind: 'info', message: 'Register markdown copied' })
  } catch {
    host.notify({ kind: 'error', message: 'Clipboard unavailable' })
  }
}

function toMarkdown(list) {
  const lines = ['# Basal register', '']
  for (const e of list) {
    lines.push(`## ${e.id} — ${e.title}`)
    lines.push(`- date: ${e.date}`)
    lines.push(`- proposer: ${e.proposer || '-'}`)
    lines.push(`- status: ${e.status}`)
    if (e.decision) lines.push(`- decision: ${e.decision}`)
    if (e.consent) lines.push(`- consent: ${e.consent}`)
    if (e.review) lines.push(`- review: ${e.review}`)
    if (e.outcome) lines.push(`- outcome: ${e.outcome}`)
    lines.push('')
  }
  return lines.join('\n')
}

// --- view ------------------------------------------------------------------
const chip = 'inline-flex items-center rounded px-1.5 py-px text-[0.6875rem] border'
const statusChip = s =>
  s === 'decided'
    ? cn(chip, 'text-(--ui-accent) border-(--ui-accent)')
    : cn(chip, 'text-(--ui-text-tertiary) border-(--ui-stroke-secondary)')

function Entry({ e, deciding }) {
  const draft = useValue(decisionDraft)
  const due = e.status === 'decided' && e.review && !e.outcome && e.review <= today()
  return jsxs('div', {
    className: 'flex flex-col gap-1 border-b border-(--ui-stroke-secondary) py-2',
    children: [
      jsxs('div', { className: 'flex items-center gap-2', children: [
        jsx('span', { className: 'font-mono text-[0.6875rem] text-(--ui-text-quaternary)', children: e.id }),
        jsx('span', { className: 'flex-1 truncate', children: e.title }),
        jsx('span', { className: statusChip(e.status), children: e.status }),
        due ? jsx('span', { className: cn(chip, 'text-(--ui-text-primary) border-(--ui-text-primary)'), children: 'review due' }) : null
      ] }),
      jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-quaternary)', children: `${e.date}${e.proposer ? ' · ' + e.proposer : ''}${e.review ? ' · review ' + e.review : ''}` }),
      e.decision ? jsx('div', { className: 'text-xs text-(--ui-text-secondary)', children: e.decision }) : null,
      e.status === 'decided' && !e.outcome
        ? jsxs('div', { className: 'flex items-center gap-1.5 pt-0.5', children: [
            jsx('span', { className: 'text-[0.6875rem] text-(--ui-text-quaternary)', children: 'outcome:' }),
            jsx('button', { className: btnSmall, type: 'button', onClick: () => review(e.id, 'worked'), children: 'worked' }),
            jsx('button', { className: btnSmall, type: 'button', onClick: () => review(e.id, 'partial'), children: 'partial' }),
            jsx('button', { className: btnSmall, type: 'button', onClick: () => review(e.id, 'failed'), children: 'failed' })
          ] })
        : null,
      e.outcome ? jsx('div', { className: 'text-xs text-(--ui-text-secondary)', children: `outcome: ${e.outcome}` }) : null,
      e.status === 'proposed' && deciding !== e.id
        ? jsx('button', { className: btnSmall, type: 'button', onClick: () => startDecide(e.id), children: 'decide…' })
        : null,
      deciding === e.id
        ? jsxs(Fragment, { children: [
            jsx('input', {
              className: inputCls,
              placeholder: 'what was decided (one sentence)',
              value: draft,
              onChange: ev => decisionDraft.set(ev.target.value)
            }),
            jsxs('div', { className: 'flex gap-1.5', children: [
              jsx('button', { className: btnSmall, type: 'button', onClick: confirmDecide, children: 'confirm (review +30d)' }),
              jsx('button', { className: btnSmall, type: 'button', onClick: () => decidingId.set(null), children: 'cancel' })
            ] })
          ] })
        : null
    ]
  })
}

const btnSmall =
  'inline-flex items-center rounded border border-(--ui-stroke-secondary) px-2 py-0.5 text-[0.6875rem] text-(--ui-text-secondary) hover:bg-(--chrome-action-hover) transition-colors'
const inputCls =
  'h-7 flex-1 rounded border border-(--ui-stroke-secondary) bg-transparent px-2 text-xs outline-none focus:border-(--ui-accent)'

function Pane() {
  const list = useValue(entries)
  const title = useValue(draftTitle)
  const proposer = useValue(draftProposer)
  const deciding = useValue(decidingId)
  const decided = list.filter(e => e.status === 'decided').length
  const due = list.filter(e => e.status === 'decided' && e.review && !e.outcome && e.review <= today()).length

  return jsxs('div', { className: 'flex h-full flex-col gap-2 p-3 text-sm', children: [
    jsxs('div', { className: 'flex items-center gap-2', children: [
      jsx('div', { className: 'font-medium', children: 'basal register' }),
      jsx('span', { className: 'text-[0.6875rem] text-(--ui-text-quaternary)', children: `${list.length} entries · ${decided} decided · ${due} reviews due` }),
      jsx('div', { className: 'ml-auto' }),
      jsx('button', { className: btnSmall, type: 'button', onClick: copyMarkdown, children: 'copy markdown' })
    ] }),
    jsxs('div', { className: 'flex items-center gap-1.5', children: [
      jsx('input', { className: inputCls, placeholder: 'proposal title', value: title, onChange: ev => draftTitle.set(ev.target.value) }),
      jsx('input', { className: inputCls, placeholder: 'proposer (optional)', value: proposer, onChange: ev => draftProposer.set(ev.target.value) }),
      jsx('button', { className: btnSmall, type: 'button', onClick: propose, children: 'propose' })
    ] }),
    list.length === 0
      ? jsx('div', { className: 'flex flex-1 items-center justify-center text-xs text-(--ui-text-quaternary)', children: 'No entries yet — propose the first BASAL-001.' })
      : jsx('div', { className: 'flex-1 overflow-auto pr-1', children: list.map(e => jsx(Entry, { key: e.id, e, deciding })) })
  ] })
}

export default {
  id: ID,
  name: 'Basal Register',
  register(ctx) {
    storage = ctx.storage
    entries.set(storage.get('entries') || [])
    ctx.register({
      id: 'pane',
      area: 'panes',
      title: 'basal register',
      data: { placement: 'bottom', dock: { pane: 'workspace', pos: 'bottom' }, height: '280px' },
      render: () => jsx(Pane, {})
    })
  }
}

// Test hook: lets a harness drive the flow without the UI (ignored by the app).
export const _test = {
  entries, draftTitle, draftProposer, decidingId, decisionDraft,
  propose, startDecide, confirmDecide, review, toMarkdown
}
