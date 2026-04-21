import { Component, OnInit } from '@angular/core';
import { ApiService, LoginResponse, UserCreate, UserUpdate } from '../services/api.service';

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
  authMode: 'login' | 'register' = 'login';
  userForm: UserCreate = {
    name: '',
    email: '',
    password: '',
  };
  editMode = false;
  editForm: UserUpdate = {
    name: '',
    email: '',
  };

  constructor(private api: ApiService) {}

  ngOnInit() {
    const user = localStorage.getItem('currentUser');
    if (user) {
      this.currentUser = JSON.parse(user);
      this.fetchTrips();
    }
  }

  toggleEdit() {
    this.editMode = !this.editMode;
    if (this.editMode) {
      this.editForm = {
        name: this.currentUser.name,
        email: this.currentUser.email,
      };
    }
    this.error = '';
  }

  saveProfile() {
    if (!this.currentUser?.token) {
      return;
    }
    this.loading = true;
    this.error = '';
    this.api.updateUser(this.editForm, this.currentUser.token).subscribe(
      (updatedUser) => {
        this.currentUser = { ...this.currentUser, ...updatedUser };
        localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
        this.editMode = false;
        this.loading = false;
      },
      (err) => {
        this.error = err?.error?.detail || 'No se pudo actualizar el perfil';
        this.loading = false;
      },
    );
  }

  fetchTrips() {
    if (!this.currentUser?.token) {
      return;
    }
    this.loading = true;
    this.api.getUserTrips(this.currentUser.token).subscribe(
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

  toggleMode() {
    this.authMode = this.authMode === 'login' ? 'register' : 'login';
    this.error = '';
  }

  submit() {
    this.error = '';
    this.loading = true;

    if (this.authMode === 'register') {
      this.api.createUser(this.userForm).subscribe(
        () => {
          this.apiLogin();
        },
        (err) => {
          this.error = err?.error?.detail || 'No se pudo crear el usuario';
          this.loading = false;
        },
      );
    } else {
      this.apiLogin();
    }
  }

  apiLogin() {
    this.api.login(this.userForm.email, this.userForm.password).subscribe(
      (response: LoginResponse) => {
        this.currentUser = { ...response.user, token: response.access_token };
        localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
        this.userForm = { name: '', email: '', password: '' };
        this.error = '';
        this.fetchTrips();
        this.loading = false;
      },
      (err) => {
        this.error = err?.error?.detail || 'No se pudo iniciar sesión';
        this.loading = false;
      },
    );
  }

  logout() {
    if (this.currentUser?.token) {
      this.api.logout(this.currentUser.token).subscribe(
        () => {
          this.performLogout();
        },
        () => {
          // Even if backend logout fails, clear local storage
          this.performLogout();
        }
      );
    } else {
      this.performLogout();
    }
  }

  private performLogout() {
    localStorage.removeItem('currentUser');
    this.currentUser = null;
    this.trips = [];
    this.error = '';
  }
}
