import { Component, Input } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { CommonService } from 'src/app/common/common.service';
import { ViewInterviewApplicantsComponent } from '../view-interview-applicants/view-interview-applicants.component';

@Component({
  selector: 'app-jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.scss']
})
export class JobsComponent {

  @Input() isHr = true;
  @Input() jobList: any[] = []

  constructor(public commonService: CommonService, private router: Router, public dialog: MatDialog){}

  openApplySideNav(job: any){
    this.commonService.jobId = job.Job_ID
    this.commonService.openApplySideNav();
  }

  openJobDetails(){
    if(!this.isHr){
      this.router.navigate(['/home/job-detail']);
    }
  }

  openViewApplicants(job: any) {
    const dialogRef = this.dialog.open(ViewInterviewApplicantsComponent, {
      width: "50%",
      data: job
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }
}
