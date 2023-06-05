import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { tap } from 'rxjs/operators';
import { LanguageData, Language, Categories, Tags, Anekdoty } from '../models/category.model';
import { CategoryDefaultService } from '../services/category-default.service';
import { LanguageService } from '../services/language.service';

@Component({
  selector: 'app-tag',
  templateUrl: './tag.component.html',
  styleUrls: ['./tag.component.scss']
})
export class TagComponent implements OnInit {
  languageUrl!: string;
  categoryUrl!: string;
  subcategoryUrl!: string;
  tagUrl!: string;
  subtagUrl!: string;
  tagData: Tags[] = [];

  constructor(
    private route: ActivatedRoute,
    private categoryService: CategoryDefaultService,
    private languageService: LanguageService,
    private tagService: CategoryDefaultService
  ) {}

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      this.languageUrl = params.get('languageUrl') || '';
      this.categoryUrl = params.get('categoryUrl') || '';
      this.subcategoryUrl = params.get('subcategoryUrl') || '';
      this.tagUrl = params.get('tagUrl') || '';
      this.subtagUrl = params.get('subtagUrl') || '';

      this.loadTagData();
    });
  }

  loadTagData() {
    this.tagService.getTagsData(this.languageUrl, this.categoryUrl, this.subcategoryUrl, this.tagUrl, this.subtagUrl)
      .pipe(
        tap((data) => {
          this.tagData = data;
        })
      )
      .subscribe({
        next: (data: Tags[]) => {
          this.tagData = data;
        },
        error: (error) => {
          console.error('Failed to load tag data:', error);
        }
      });
  }
}
