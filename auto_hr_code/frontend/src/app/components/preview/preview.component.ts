import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { SnackbarComponent } from '../snackbar/snackbar.component';
import { CommonService } from 'src/app/common/common.service';

@Component({
  selector: 'app-preview',
  templateUrl: './preview.component.html',
  styleUrls: ['./preview.component.scss']
})
export class PreviewComponent {
  
  jobData: any;
  previewResponse: any;

  constructor(private router: Router, private _snackBar: MatSnackBar, public commonService: CommonService){}

  ngOnInit(){
    const jobdata = localStorage.getItem('jobdata');
    if(jobdata){
      this.jobData = JSON.parse(jobdata);
      this.getJobPreView();
    }
  }

  getJobPreView(){
    this.commonService.isLoaderShow = true;
    const data = {
      Job: this.jobData.Job,
      About_Company: this.jobData?.About_Company,
      Job_Description: this.jobData?.Job_Description
      };

    this.commonService.previewJob(data).subscribe((response: any) => {
      if(response){
        this.previewResponse = response;
    this.commonService.isLoaderShow = false;
      }
    });
  }

  backtoJobList(){
    this.commonService.isLoaderShow = true;

    const data = {
      Job: this.jobData.Job,
      Job_Description: this.jobData?.Job_Description,
      About_Company: this.jobData?.About_Company,
      Job_Summary: this.jobData?.Job_Summary ?? '' 
    };

    this.commonService.postNewJob(data).subscribe((response: any) => {
      if(response){
        this.router.navigate(['/home/hrjobs']);
        this._snackBar.openFromComponent(SnackbarComponent, {
          horizontalPosition: 'end',
          verticalPosition: 'top',
          duration: 5000,
          panelClass: ['bgd-color'],
        });

        localStorage.removeItem('jobdata');
        this.commonService.isLoaderShow = false;
      }
    })

  }


  insertNewData(name: string){
    if(name === 'description'){
      this.jobData.Job_Description = this.previewResponse.Job_Description;
    } else if(name === 'about'){
      this.jobData.About_Company = this.previewResponse.About_Company;
    } else if(name === 'summary'){
      this.jobData['Job_Summary'] = this.previewResponse.Job_Summary;
    }
  }

  CancelPostJob(){
    localStorage.removeItem('jobdata');
    this.router.navigate(['/home/hrjobs']);
  }
}


