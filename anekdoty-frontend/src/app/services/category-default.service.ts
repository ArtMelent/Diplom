import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Language, LanguageData, Categories } from '../models/category.model';

@Injectable({
  providedIn: 'root'
})
export class CategoryDefaultService {
  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) { }

  getLanguageDataByUrl(language: Language): Observable<LanguageData> {
    const url = `${this.apiUrl}/${language.url}`;
    return this.http.get<LanguageData>(url);
  }

  getSharedCategoryData(languageId: number): Observable<Categories[]> {
    const url = `${this.apiUrl}/category/shared-data/for/me/url?langUrl=${languageId}`;

    return this.http.get<Categories[]>(url).pipe(
      catchError((error: any) => {
        // Handle error
        console.error('An error occurred:', error);
        // You can throw a custom error or return a default value here
        throw new Error('Unable to fetch category data');
      })
    );
  }

  getCategoryData(languageUrl: string, categoryUrl: string, subcategoryUrl?: string): Observable<any> {
    let url = `${this.apiUrl}/${languageUrl}/${categoryUrl}/`;
    if (subcategoryUrl) {
      url += `${subcategoryUrl}/`;
    }
    return this.http.get<any>(url).pipe(
      catchError(this.handleError)
    );
  }

  getTagsData(languageUrl: string, categoryUrl: string, subcategoryUrl?: string, tagUrl?: string, subtagUrl?: string): Observable<any> {
    let url = `${this.apiUrl}/${languageUrl}/${categoryUrl}`;

    if (subcategoryUrl) {
      url += `/${subcategoryUrl}`;
    }

    if (tagUrl) {
      url += `/${tagUrl}`;

      if (subtagUrl) {
        url += `/${subtagUrl}`;
      }
    }

    return this.http.get<any>(url).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: any): Observable<any> {
    console.error('An error occurred:', error);
    return of(null);
  }
}
