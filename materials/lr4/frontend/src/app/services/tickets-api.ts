import { Injectable } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { Equipment, Stats, Ticket, TicketEvent, TicketInput, TicketStatus } from '../models/ticket';
@Injectable({providedIn:'root'})
export class TicketsApi {
  // TODO(LR4-02): внедрите HttpClient и реализуйте методы по контракту API.
  private pending<T>():Observable<T> {return throwError(()=>new Error('Выполните LR4-02'));}
  list(q='',mode='all'):Observable<Ticket[]> {return this.pending();}
  get(id:number):Observable<Ticket> {return this.pending();}
  create(input:TicketInput):Observable<Ticket> {return this.pending();}
  update(id:number,input:TicketInput & {status:TicketStatus}):Observable<Ticket> {return this.pending();}
  delete(id:number):Observable<void> {return this.pending();}
  equipment():Observable<Equipment[]> {return this.pending();}
  stats():Observable<Stats> {return this.pending();}
  events(id:number):Observable<TicketEvent[]> {return this.pending();}
}
export function errorMessage(error:unknown):string {
  // TODO(LR4-03): различите сетевую ошибку и JSON-ошибку сервера.
  return 'Не удалось выполнить запрос. Повторите попытку.';
}
