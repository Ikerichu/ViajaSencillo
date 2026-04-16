import { Component, OnInit } from '@angular/core';
import { ApiService, UserCreate } from '../services/api.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css'],
})
export class ProfileComponent implements OnInit {
  currentUser: any = null;
  trips: any[] = [];
  loading = false;
  error = '';
  userForm: UserCreate = {
    name: '',
    email: '',
    password: '',
  };

  constructor(private api: ApiService) {}

  ngOnInit() {
    const user = localStorage.getItem('currentUser');
    if (user) {
      this.currentUser = JSON.parse(user);
      this.fetchTrips();
    }
  }

  fetchTrips() {
    if (!this.currentUser) {
      return;
    }
    this.loading = true;
    this.api.getUserTrips(this.currentUser.id).subscribe(
      (trips) => {
        this.trips = trips;
        this.loading = false;
      },
      () => {
        this.error = 'No se pudieron cargar los viajes del usuario';
        this.loading = false;
      },
    );
  }

  submit() {
    this.error = '';
    this.loading = true;
    this.api.createUser(this.userForm).subscribe(
      (user) => {
        this.currentUser = user;
        localStorage.setItem('currentUser', JSON.stringify(user));
        this.userForm = { name: '', email: '', password: '' };
        this.fetchTrips();
      },
      (err) => {
        this.error = err?.error?.detail || 'No se pudo crear el usuario';
        this.loading = false;
      },
    );
  }

  logout() {
    localStorage.removeItem('currentUser');
    this.currentUser = null;
    this.trips = [];
  }
}
