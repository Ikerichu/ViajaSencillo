import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService, PlannerRequest } from '../services/api.service';

@Component({
  selector: 'app-planner',
  templateUrl: './planner.component.html',
  styleUrls: ['./planner.component.css'],
})
export class PlannerComponent implements OnInit {
  destination = 'Madrid';
  start_date = '';
  end_date = '';
  budget = 800;
  interests = {
    comida: false,
    cultura: false,
    naturaleza: false,
    fiesta: false,
  };
  destinations: string[] = [];
  loading = false;
  error = '';

  constructor(private api: ApiService, private router: Router) {}

  ngOnInit() {
    this.api.getDestinations().subscribe((data) => {
      this.destinations = data;
      if (data.length) {
        this.destination = data[0];
      }
    });
  }

  submit() {
    this.error = '';
    this.loading = true;
    const interests = (Object.keys(this.interests) as Array<keyof typeof this.interests>).filter(
      (key) => this.interests[key],
    );
    const request: PlannerRequest = {
      destination: this.destination,
      start_date: this.start_date,
      end_date: this.end_date,
      budget: this.budget,
      interests,
    };

    this.api.generatePlanner(request).subscribe(
      (result) => {
        const storedResult: any = { ...result, savedMessage: '', saved: false };
        const currentUser = JSON.parse(localStorage.getItem('currentUser') || 'null');

        if (currentUser && currentUser.token) {
          const tripPayload = {
            ...request,
            itinerary: result.itinerary,
          };

          this.api.saveTrip(tripPayload, currentUser.token).subscribe(
            () => {
              storedResult.saved = true;
              storedResult.savedMessage = 'Viaje guardado para el usuario ' + currentUser.name;
              localStorage.setItem('plannerResult', JSON.stringify(storedResult));
              this.router.navigate(['/results']);
            },
            () => {
              storedResult.savedMessage = 'No se pudo guardar el viaje en el servidor.';
              localStorage.setItem('plannerResult', JSON.stringify(storedResult));
              this.router.navigate(['/results']);
            },
          );
        } else {
          localStorage.setItem('plannerResult', JSON.stringify(storedResult));
          this.router.navigate(['/results']);
        }
      },
      (err) => {
        this.error = err?.error?.detail || 'No se pudo generar el itinerario';
        this.loading = false;
      },
    );
  }
}
