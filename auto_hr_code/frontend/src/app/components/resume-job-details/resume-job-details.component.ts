import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { SnackbarComponent } from '../snackbar/snackbar.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CommonService } from 'src/app/common/common.service';

@Component({
  selector: 'app-resume-job-details',
  templateUrl: './resume-job-details.component.html',
  styleUrls: ['./resume-job-details.component.scss']
})
export class ResumeJobDetailsComponent {

  resumeDetail: any;
  jobDetails: any;

  constructor(private router: Router, private _snackBar: MatSnackBar, public commonService: CommonService){}


  ngOnInit(){
    this.getAllApplications();
    this.getAllJobs();
  }
  getAllApplications(){
    this.commonService.getAllApplcationList().subscribe((response: any) => {
      if(response){
        const applicationList = response as Array<any>;
        this.resumeDetail = applicationList.find(item => item.Application_ID === this.commonService.applicationId);
        console.log(this.resumeDetail);

      }
    })
  }

  getAllJobs(){
    this.commonService.getAllJobs().subscribe((response: any) => {
      if(response){
        const jobList = response as Array<any>;
        this.jobDetails = jobList.find(item => item.Job_ID === this.commonService.jobId);
      }
    })
  }

  backtoJobList(){
    this.router.navigate(['/home/candidatejobs']);
   
  }

  getScore(score: number){
    return score / 100 * 10;
  }
}
