import { openDB } from 'idb';
import type { Pack, Result } from '../types';

const db = openDB('offlinemock', 1, { upgrade(database) { database.createObjectStore('packs', { keyPath: 'id' }); database.createObjectStore('results', { keyPath: 'packId' }); database.createObjectStore('preferences', { keyPath: 'key' }); } });
export const storePack = (pack: Pack) => db.then(d => d.put('packs', pack));
export const getPacks = () => db.then(d => d.getAll('packs') as Promise<Pack[]>);
export const getPack = (id: string) => db.then(d => d.get('packs', id) as Promise<Pack | undefined>);
export const deletePack = (id: string) => Promise.all([db.then(d => d.delete('packs', id)), db.then(d => d.delete('results', id))]);
export const saveResult = (result: Result) => db.then(d => d.put('results', result));
export const getResult = (id: string) => db.then(d => d.get('results', id) as Promise<Result | undefined>);
export const savePreference = (key: string, value: unknown) => db.then(d => d.put('preferences', { key, value }));
export const getPreference = (key: string) => db.then(d => d.get('preferences', key) as Promise<{ key: string; value: unknown } | undefined>);
