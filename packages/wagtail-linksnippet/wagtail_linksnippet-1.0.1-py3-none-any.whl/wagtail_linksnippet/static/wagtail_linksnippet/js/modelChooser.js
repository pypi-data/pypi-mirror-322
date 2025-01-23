(function () {

    window.modelChooserConfigs = window.modelChooserConfigs || [];

    $.fn.chooserLinks = function() {
        return this.find('a[data-chooser-modal-choice]');
    };

    $.fn.paginationLinks = function() {
        return this.find('nav.pagination a');
    };

    $.fn.onChooserLinksClick = function(callback) {
        return this.chooserLinks().on('click', function(e) {
            e.preventDefault();
            const $currentTarget = $(e.currentTarget);
            const data = $currentTarget.data();
            data.href = $currentTarget.attr('href');
            data.anchorText = $currentTarget.text();
            callback(data);
        });
    };

    $.fn.onPaginationLinksClick = function(callback) {
        return this.paginationLinks().on('click', function(e) {
            e.preventDefault();
            const href = $(e.currentTarget).attr('href');
            $.get(href, (data) => {
                callback(data);
            });
        });
    };    

    function initModelChooser() {
        window.modelChooserConfigs.forEach(function(config) {
        
            const React = window.React;

            class ModelSource extends React.Component {
        
                searchInputSelectors = '#id_q';
                searchFormSelector = 'form[data-chooser-modal-search]';
                searchForm = null;
                searchUrl = null;
                searchResults = null;

                componentDidMount() {
                    const { onClose, editorState, entityType, onComplete } = this.props;
                    const ModalWorkflow = window.ModalWorkflow;
                    
                    this.onClose = onClose;
        
                    ModalWorkflow({
                        url: config.chooserUrl,
                        onload: {
                            choose: this.onModalLoad,
                        },
                        responses: {
                            close: onClose,
                            chosen: this.onChosen,
                        },
                        onError: (err) => {
                            console.error('Errore nella modale Campaign Chooser:', err);
                            onClose();
                        },
                    });
                }
        
                onModalLoad = (modal, jsonData) => {
                    this.searchForm = $(this.searchFormSelector, modal.body);
                    this.searchUrl = this.searchForm.attr('action');
                    this.searchResults = $('#search-results', modal.body);

                    this.setupCloseButton(modal);
                    this.setupSearchFunctionality(modal);
                };
        
                setupCloseButton(modal) {
                    const { onClose } = this.props;
                    modal.container.on('click', 'button.button.close', function () {
                        onClose();
                    });
                }
        
                getSearchFormData() {
                    return this.searchForm.serialize();
                }

                setupSearchFunctionality(modal) {
                    const $searchResults = this.searchResults;
        
                    this.searchForm.on('submit', (e) => {
                        e.preventDefault();
                        this.performSearch(modal);
                    });
        
                    this.ajaxifyLinks($searchResults, modal);
                    this.attachSearch(modal);
            
                }
        
                updateResults(data, modal) {
                    this.searchResults.html(data);
                    this.ajaxifyLinks(this.searchResults, modal);
                }
        
                performSearch(modal) {
                    const data = this.getSearchFormData()
                    $.get(this.searchUrl, data, (response) => {
                        this.updateResults(response, modal);
                    });
                }
        
                attachSearch(modal) {
                    const inputDelay = 200;
                    let timer;
                    
                    $(this.searchInputSelectors, modal.container).on('input', (e) => {
                        let request = null;

                        if (request) {
                            request.abort();
                        }

                        clearTimeout(timer);
                        
                        timer = setTimeout(() => {
                            this.performSearch(modal);
                        }, inputDelay);

                    });

                    $(this.searchInputSelectors, modal.container).trigger('focus');

                }

                ajaxifyLinks($container, modal) {
                    $container.onChooserLinksClick((data) => {
                        modal.respond('chosen', data);
                        modal.close();
                    });
                    $container.onPaginationLinksClick((data) => {
                        $container.html(data);
                        this.ajaxifyLinks($container, modal);
                    });
                }
        
                filterEntityData(data) {
                    let id = data.id;
                    
                    if (!id && data.href) {
                        const href = data.href;
                        const idMatch = href.match(/\/(\d+)\/?$/);
                        id = idMatch ? idMatch[1] : null;
                    }

                    return {
                        string: data.string || data.anchorText,
                        id: id,          
                        app_name: config.appName,
                        model_name: config.modelName,
                    };
                }
            
                onChosen = (data) => {
                    const { editorState, entityType, onComplete } = this.props;
                    const Modifier = window.DraftJS.Modifier;
                    const EditorState = window.DraftJS.EditorState;
                    const content = editorState.getCurrentContent();
                    const selection = editorState.getSelection();
                    const entityData = this.filterEntityData(data);
        
                    const selectedText = content.getBlockForKey(selection.getStartKey())
                        .getText()
                        .slice(
                            selection.getStartOffset(),
                            selection.getEndOffset()
                        );
                        
                    const text = selectedText || data.string;
        
                    const contentWithEntity = content.createEntity(
                        entityType.type,
                        'MUTABLE',
                        entityData,
                    );
                    const entityKey = contentWithEntity.getLastCreatedEntityKey();
        
                    const newContent = Modifier.replaceText(
                        contentWithEntity,
                        selection,
                        text,
                        null,
                        entityKey,
                    );
        
                    const nextState = EditorState.push(
                        editorState,
                        newContent,
                        'insert-characters',
                    );
                    
                    onComplete(nextState);
        
                };
        
                render() {
                    return null;
                }
            }
        
            const ModelEntity = (props) => {
                const { entityKey, contentState } = props;
                const data = contentState.getEntity(entityKey).getData();
                const TooltipEntity = window.draftail.TooltipEntity;
        
                let icon = React.createElement(window.wagtail.components.Icon, {name: config.iconName});
                let label = data.string || `Edit ${data.model_name}`;
        
                return window.React.createElement(
                    TooltipEntity,
                    {
                        entityKey: props.entityKey,
                        children: props.children,
                        onEdit: props.onEdit,
                        onRemove: props.onRemove,
                        icon: icon,
                        label: label,
                    },
                    props.children,
                );
            };
            
            window.draftail.registerPlugin({
                type: config.typeName,
                source: ModelSource,
                decorator: ModelEntity,
            }, 'entityTypes');
        

        });
    }

    function safeInitModelChooser() {
        if (window.draftail) {
            initModelChooser();
        } else {
            setTimeout(safeInitModelChooser, 100);
        }
    }

    window.safeInitModelChooser = safeInitModelChooser;

})();
