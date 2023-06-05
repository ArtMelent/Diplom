import { Component, OnInit } from '@angular/core';
import { Categories, Language } from '../models/category.model';
import { CategoryDefaultService } from '../services/category-default.service';
import { LanguageService } from '../services/language.service';

@Component({
  selector: 'app-test-slidebar',
  templateUrl: './test-slidebar.component.html',
  styleUrls: ['./test-slidebar.component.scss']
})
export class TestSlidebarComponent implements OnInit {
  categories: Categories[] = [];
  language: Language | null = null;

  constructor(
    private categoryService: CategoryDefaultService,
    private languageService: LanguageService
  ) {}

  ngOnInit(): void {
    this.languageService.getSelectedLanguage().subscribe(language => {
      if (language) {
        console.log(language.url)
        this.language = language;
        this.fetchSharedCategoryData();
      }
    });
  }

  fetchSharedCategoryData(): void {
    if (this.language) {
      this.categoryService.getSharedCategoryData(this.language.id).subscribe({
        next: (data: Categories[]) => {
          this.categories = data;
        },
        error: (error: any) => {
          // Handle error
          console.error('An error occurred:', error);
        }
      });
    }
  }
}
