import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';

import {MatButtonModule} from '@angular/material/button';
import {MatRadioModule} from '@angular/material/radio';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatDialogModule} from '@angular/material/dialog';

import { NgCircleProgressModule } from 'ng-circle-progress';

import { JoinAsComponent } from './components/join-as/join-as.component';
import { HeaderComponent } from './components/header/header.component';
import { HrJobsComponent } from './components/hr-jobs/hr-jobs.component';
import { CandidateJobsComponent } from './components/candidate-jobs/candidate-jobs.component';
import { HomeComponent } from './components/home/home.component';
import { JobsComponent } from './components/jobs/jobs.component';
import { PostNewJobComponent } from './components/post-new-job/post-new-job.component';
import { PreviewComponent } from './components/preview/preview.component';
import { UploadResumeComponent } from './components/upload-resume/upload-resume.component';
import { JobDetailsComponent } from './components/job-details/job-details.component';
import { ResumeJobDetailsComponent } from './components/resume-job-details/resume-job-details.component';
import { SkillScoreComponent } from './components/skill-score/skill-score.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CandidateNumberComponent } from './components/candidate-number/candidate-number.component';
import { InterviewComponent } from './components/interview/interview.component';
import { ViewInterviewApplicantsComponent } from './components/view-interview-applicants/view-interview-applicants.component';

@NgModule({
  declarations: [
    AppComponent,
    JoinAsComponent,
    HeaderComponent,
    HrJobsComponent,
    CandidateJobsComponent,
    HomeComponent,
    JobsComponent,
    PostNewJobComponent,
    PreviewComponent,
    UploadResumeComponent,
    JobDetailsComponent,
    ResumeJobDetailsComponent,
    SkillScoreComponent,
    CandidateNumberComponent,
    InterviewComponent,
    ViewInterviewApplicantsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatRadioModule,
    MatSidenavModule,
    MatFormFieldModule,
    MatInputModule,
    MatSnackBarModule,
    NgCircleProgressModule.forRoot(),
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    MatDialogModule
  ],
  providers: [],
  bootstrap: [AppComponent],
  entryComponents: [CandidateJobsComponent, ViewInterviewApplicantsComponent]
})
export class AppModule { }
