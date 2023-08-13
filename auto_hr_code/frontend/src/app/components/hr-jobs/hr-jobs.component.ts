import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { CommonService } from 'src/app/common/common.service';
import { CandidateNumberComponent } from '../candidate-number/candidate-number.component';

@Component({
  selector: 'app-hr-jobs',
  templateUrl: './hr-jobs.component.html',
  styleUrls: ['./hr-jobs.component.scss']
})
export class HrJobsComponent {


  isHr = true;
  jobList = [];
  constructor(public commonService: CommonService, public dialog: MatDialog){

  }

  ngOnInit(){
    this.getHrJobs();
  }

  openPostJob(){
    this.commonService.toggle();
  }


  public getHrJobs(){
    this.commonService.getAllJobs().subscribe((response: any) => {
      this.jobList = response;
    })
  }


  openCandidateDialog(){
    const dialogRef = this.dialog.open(CandidateNumberComponent);

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }
}
