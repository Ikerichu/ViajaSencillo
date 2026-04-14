import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css'],
})
export class ResultsComponent implements OnInit {
  result: any = null;

  ngOnInit() {
    const item = localStorage.getItem('plannerResult');
    this.result = item ? JSON.parse(item) : null;
  }
}
