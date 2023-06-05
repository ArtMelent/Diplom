import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CategoryDefaultService } from '../services/category-default.service';
import { tap } from 'rxjs';
import { Language, LanguageData } from '../models/category.model';
import { LanguageService } from '../services/language.service';


@Component({
  selector: 'app-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.scss']
})
export class CategoryComponent implements OnInit {
  langUrl!: string;
  categoryUrl!: string;
  subcategoryUrl!: string;
  categoryData: any;
  languageData: LanguageData[] = [];

  constructor(
    private route: ActivatedRoute,
    private categoryService: CategoryDefaultService,
    private languageService: LanguageService
  ) { }

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      this.langUrl = params.get('langUrl') || '';
      this.categoryUrl = params.get('category_url') || '';
      this.subcategoryUrl = params.get('subcategory_url') || '';
      
      if (this.langUrl) {
        const language: Language = { id: 0, code: '', name: '', url: this.langUrl };
        this.loadCategoryData(language);
      }
    });
  }

  loadCategoryData(language: Language) {
    this.categoryService.getCategoryData(this.langUrl, this.categoryUrl, this.subcategoryUrl)
      .pipe(
        tap(data => {
          this.categoryData = data;
          this.categoryData.category.subcategories = data.subcategories;
        })
      )
      .subscribe({
        next: (data: LanguageData) => {
          this.languageData = [data];
          language.id = data.language.id; // Update the language ID
          language.code = data.language.code; // Update the language code
          language.name = data.language.name; // Update the language name
          this.languageService.setSelectedLanguage(language); // Set the selected language
        },
        error: error => {
          console.error('Failed to load category data:', error);
        }
      });
  }
  
}
