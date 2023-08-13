import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class CommonService {

  public sidenav: any;
  public applySidenav: any
  jobId = '';
  applicationId = '';

  isLoaderShow = false;
  

  constructor(private httpClient: HttpClient) {}

  public open() {
    this.sidenav.open();
  }

  public close() {
    this.sidenav.close();
  }

  public toggle(): void {
    this.sidenav.toggle();
  }


  public openApplySideNav() {
    this.applySidenav.open();
  }

  public closeApplySideNav() {
    this.applySidenav.close();
  }

  public toggleApllySideNav(): void {
    this.applySidenav.toggle();
  }

  public getAllJobs(): Observable<any>{
    return this.httpClient.get(`${environment.API_URL}/jobs/get_jobs/`);
  }

  public previewJob(jobData: any): Observable<any> {
    return this.httpClient.post(`${environment.API_URL}/jobs/post_job_preview/`, jobData);
  }

  public postNewJob(jobData: any): Observable<any> {
    return this.httpClient.post(`${environment.API_URL}/jobs/post_jobs/`, jobData);
  }

  public applyJob(data: any):Observable<any> {
    return this.httpClient.post(`${environment.API_URL}/jobs/post_application/`, data);
  }

  public getSuggestions(data: any): Observable<any> {
    return this.httpClient.post(`${environment.API_URL}/jobs/get_suggestions/`, data);
  }

  public getAllApplcationList():Observable<any> {
    return this .httpClient.get(`${environment.API_URL}/jobs/get_all_applications/`);
  }

  public sendMail(count: number): Observable<any>{
    return this.httpClient.post(`${environment.API_URL}/jobs/send_emails/?k=${count}`, {});
  }

  public interview(applicationId: any, data: any): Observable<any> {
    return this.httpClient.post(`${environment.API_URL}/jobs/interview/${applicationId}/`, data);
  }

  public getInterviewByJobId(jobId: string): Observable<any> {
    return this.httpClient.get(`${environment.API_URL}/jobs/get_interviews_for_job/${jobId}/`);
  }

  public evaluate_interview(applicationId: string): Observable<any> {
    return this.httpClient.post(`${environment.API_URL}/jobs/evaluate_interview/${applicationId}/`, {});
  }

}
