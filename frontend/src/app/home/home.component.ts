import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  destinations: string[] = [];
  loading = false;
  error = '';
  features = [
    { title: 'Itinerarios automáticos', description: 'Genera planes diarios según tu presupuesto y tus intereses.' },
    { title: 'Intereses personalizados', description: 'Elige entre comida, cultura, naturaleza o fiesta.' },
    { title: 'Presupuesto optimizado', description: 'Distribuye tu dinero por día y evita sorpresas.' },
  ];

  constructor(private router: Router, private api: ApiService) {}

  ngOnInit() {
    this.loading = true;
    this.api.getDestinations().subscribe(
      (data) => {
        this.destinations = data;
        this.loading = false;
      },
      () => {
        this.error = 'No se pudieron cargar los destinos en este momento.';
        this.loading = false;
      },
    );
  }

  goToPlanner() {
    this.router.navigate(['/planner']);
  }
}
