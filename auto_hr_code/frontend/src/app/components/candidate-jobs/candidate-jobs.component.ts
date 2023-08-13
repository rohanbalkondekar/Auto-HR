import { Component } from '@angular/core';
import { CommonService } from 'src/app/common/common.service';

@Component({
  selector: 'app-candidate-jobs',
  templateUrl: './candidate-jobs.component.html',
  styleUrls: ['./candidate-jobs.component.scss']
})
export class CandidateJobsComponent {

  isHr = false;
  jobList: any;

  constructor(private commonSerivce: CommonService){}

  ngOnInit(){
    this.getHrJobs();
  }

  public getHrJobs(){
    this.commonSerivce.getAllJobs().subscribe((response: any) => {
      this.jobList = response;

    })
  }
}
