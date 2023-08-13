import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { CommonService } from 'src/app/common/common.service';
import { SnackbarComponent } from '../snackbar/snackbar.component';

@Component({
  selector: 'app-upload-resume',
  templateUrl: './upload-resume.component.html',
  styleUrls: ['./upload-resume.component.scss'],
})
export class UploadResumeComponent {
  name = '';
  email = '';
  contact = '';
  writeAResume = '';
  resume: any;
  file: any;
  suggestionResponse: any;

  constructor(
    public commonService: CommonService,
    private router: Router,
    private _snackBar: MatSnackBar
  ) {}

  closeSideNav() {
    this.commonService.closeApplySideNav();
  }

  openFileChooser() {
    document.getElementById('file-chooser-resume')?.click();
  }

  onFileSelect(event: any) {
    this.file = event.target.files[0];
    console.log(this.file);

    if (this.file.type === 'text/plain') {
      let fileReader = new FileReader();
      fileReader.onload = (e) => {
        this.resume = fileReader?.result;
      };
      fileReader.readAsText(this.file);
    } else if (this.file.type === 'application/pdf') {
    } else if (
      this.file.type ===
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ) {
    }
  }

  openJobPreview() {
    // this.closeSideNav();
    // this.router.navigate(['/home/resume-job-detail'])

    this.getSuggestions();
  }

  public getSuggestions() {
    this.commonService.isLoaderShow = true;
    const data = {
      Job_ID: this.commonService.jobId,
      Resume: this.resume ? this.resume : this.writeAResume,
    };

    this.commonService.getSuggestions(data).subscribe((response: any) => {
      if (response) {
        this.suggestionResponse = response;
        this.applyForNewJob();
      }
    });
  }

  public applyForNewJob() {
    const data = {
      Job_ID: this.commonService.jobId,
      Name: this.name,
      Email: this.email,
      Contact: this.contact,
      Resume: this.resume,
      Resume_Summary: this.suggestionResponse.Resume_Summary,
      Improvements: this.suggestionResponse.Improvements,
      Screening_Questions: this.suggestionResponse.Screening_Questions,
      Answers: [
        'I worked with Actix Web framework',

        'I worked with Redis',

        'I worked on large scale Synthetic data generatation',

        'Not Much',

        'Not Much',
      ],
    };

    // console.log(data);
    // return;

    this.commonService.applyJob(data).subscribe((response: any) => {
      if (response) {
        this.commonService.applicationId = response.Application_ID;
        this.closeSideNav();
        this._snackBar.openFromComponent(SnackbarComponent, {
          horizontalPosition: 'end',
          verticalPosition: 'top',
          duration: 5000,
          panelClass: ['bgd-color'],
        });
        this.commonService.isLoaderShow = false;
        this.router.navigate(['/home/resume-job-detail']);

        this.name = '';
        this.email = '';
        this.contact = '';
        this.writeAResume = '';
        this.file = null;
      }
    });
  }

  removeFile() {
    this.file = null;
  }

  validateForm() {
    if (
      this.name &&
      this.email &&
      this.contact &&
      (this.resume || this.writeAResume)
    ) {
      return true;
    }
    return false;
  }
}
