# mysite contain...........
models --- Post , Comments
forms ---- SearchForm,EmailPostForm,CommentForm
newfile --- feeds.py,sitemaps.py
template --- blog_tags.py(custom template)---simpletag,inclusiontag,filtertag
database -- postgres(integration)


functionality ----- sitemaps/rssfeedback/tags/comments/postgres_powerfull_searchengine(SearchVector/ TrigramSimilarity/)
basic functionality -- postlist(generic list view/simple list view)
                    --postdetails
                    --paginator
                    --rssfeed integration
                    
additional app --- taggit
internal app --  sitemaps,postgres
