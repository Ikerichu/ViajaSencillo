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
        localStorage.setItem('plannerResult', JSON.stringify(result));
        this.router.navigate(['/results']);
      },
      (err) => {
        this.error = err?.error?.detail || 'No se pudo generar el itinerario';
        this.loading = false;
      },
    );
  }
}
