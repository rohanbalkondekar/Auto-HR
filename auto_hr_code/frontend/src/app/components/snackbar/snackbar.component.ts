import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatSnackBar, MatSnackBarRef } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

@Component({
  selector: 'app-snackbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './snackbar.component.html',
  styleUrls: ['./snackbar.component.scss']
})
export class SnackbarComponent {
  isHrJobLoaded = true;
  constructor(private snackbarRef: MatSnackBarRef<SnackbarComponent>, private router: Router){

    this.isHrJobLoaded = this.router.url.includes('resume-job-detail') || this.router.url.includes('candidatejobs');
  }

  dismiss(){
    this.snackbarRef.dismiss();
  }
}
