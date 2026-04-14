import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface PlannerRequest {
  destination: string;
  start_date: string;
  end_date: string;
  budget: number;
  interests: string[];
}

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getDestinations(): Observable<string[]> {
    return this.http.get<string[]>(`${this.baseUrl}/destinations`);
  }

  getPlaces(destination: string, interests: string[]): Observable<any> {
    let params = new HttpParams().set('destination', destination);
    if (interests.length) {
      params = params.set('interests', interests.join(','));
    }
    return this.http.get(`${this.baseUrl}/places`, { params });
  }

  generatePlanner(request: PlannerRequest): Observable<any> {
    return this.http.post(`${this.baseUrl}/planner`, request);
  }
}
