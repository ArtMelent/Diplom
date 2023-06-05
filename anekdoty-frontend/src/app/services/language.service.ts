import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, map } from 'rxjs';
import { Language } from '../models/category.model';

@Injectable({
  providedIn: 'root'
})
export class LanguageService {
  private selectedLanguageSubject: BehaviorSubject<Language | null> = new BehaviorSubject<Language | null>(null);

  setSelectedLanguage(language: Language): void {
    this.selectedLanguageSubject.next(language);
  }

  getSelectedLanguage(): Observable<Language | null> {
    return this.selectedLanguageSubject.asObservable();
  }

  getSelectedLanguageId(): Observable<number | null> {
    return this.selectedLanguageSubject.asObservable().pipe(
      map(language => (language ? language.id : null))
    );
  }
}

