import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { JoinAsComponent } from './components/join-as/join-as.component';
import { HomeComponent } from './components/home/home.component';
import { HrJobsComponent } from './components/hr-jobs/hr-jobs.component';
import { CandidateJobsComponent } from './components/candidate-jobs/candidate-jobs.component';
import { PreviewComponent } from './components/preview/preview.component';
import { JobDetailsComponent } from './components/job-details/job-details.component';
import { ResumeJobDetailsComponent } from './components/resume-job-details/resume-job-details.component';
import { InterviewComponent } from './components/interview/interview.component';

const routes: Routes = [
  {
    path: 'joinas', component: JoinAsComponent
  },
  {
    path: '', redirectTo: 'joinas', pathMatch: 'full'
  },
  {
    path: 'home', component: HomeComponent,
    children: [
      {
        path: 'hrjobs', component: HrJobsComponent
      },
      {
        path: 'candidatejobs', component: CandidateJobsComponent
      },
      {
        path: 'preview', component: PreviewComponent
      },
      {
        path: 'job-detail', component: JobDetailsComponent
      },
      {
        path: 'resume-job-detail', component: ResumeJobDetailsComponent
      }
    ]
  },
  {
    path: 'interview', component: InterviewComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
