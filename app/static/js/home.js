/**
 * JavaScript file for the People page
 */

/* jshint esversion: 8 */

/**
 * This is the model class which provides access to the server REST API
 * @type {{}}
 */
class Model {
    /*ImageRead
      Annotate
      UndoLast
      BuildDatabase*/
      async imageRead(qtde, related = null, annotated = null) {
        let options = {
            method: "GET",
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json",
                "accepts": "application/json"
            }
        };
        // Call the REST endpoint and wait for data
        let callBase = `/api/database`;

        if (annotated != null){
            if (related !=  null){
                callBase = callBase.concat(`?related=${related}`)
                callBase = callBase.concat(`&annotated=${annotated}`)
            }else{
                callBase = callBase.concat(`?annotated=${annotated}`)
            }
            callBase = callBase.concat(`&qtde=${qtde}`)
        }else{
            callBase = callBase.concat(`?qtde=${qtde}`)
        }

        let response = await fetch(callBase, options);
        let data = await response.json();
        return data; 
      }

      async imageAnnotate(imagepath, image) {
        let options = {
            method: "PUT",
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json",
                "accepts": "application/json"
            },
            body: JSON.stringify(image)
        };
        // Call the REST endpoint and wait for data
        let callBase = `/api/image/${imagepath}`

        let response = await fetch(callBase, options);
        let data = await response.json();
        return data; 
      }

      async UndoLast() {
        let options = {
            method: "PUT",
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json",
                "accepts": "application/json"
            }
        };
        // Call the REST endpoint and wait for data
        let response = await fetch("/api/image/undo_last", options);
        let data = await response.json();
        return data;
      }

      async buildDatabase() {
        let options = {
            method: "POST",
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json",
                "accepts": "application/json"
            }
        };
        // Call the REST endpoint and wait for data
        let response = await fetch("/api/database", options);
        let data = await response.json();
        return data;
      }

}


/**
 * This is the view class which provides access to the DOM
 */
class View {
    /* constructor
       showImage
    */
    constructor() {
        this.error = document.querySelector(".error");
        this.undoLastButton = document.getElementById("undolast");
        this.relatedButton = document.getElementById("related");
        this.notRelatedButton = document.getElementById("notrelated");
        this.image = document.getElementById("imgid")
    }

    loadImage(imagepath) {
        this.image.src = `/static/dataset/${imagepath}`
    }

    errorMessage(message) {
        /*this.error.innerHTML = message;
        this.error.classList.add("visible");
        this.error.classList.remove("hidden");
        setTimeout(() => {
            this.error.classList.add("hidden");
            this.error.classList.remove("visible");
        }, 2000);*/
        console.log(message)
    }
}


/**
 * This is the controller class for the user interaction
 */
class Controller {
    constructor(model, view) {
        this.model = model;
        this.view = view;

        this.initialize();
    }

    async initialize() {
    /* 
    */
        await this.initializeImg()
        await this.initializeUndoLast()
        await this.initializeRelated()
        await this.initializeNotRelated()
    }

    async initializeImg() {
        try{
            let imageGet = await this.model.imageRead(1, null, false);

            this.view.loadImage(imageGet[0].imagepath)
        } catch (err) {
            this.view.errorMessage(err);
        }
    }

    async initializeUndoLast() {
        document.getElementById("undolast").addEventListener("click", async (evt) => {
            evt.preventDefault();
            try {
                let undoneImage = await this.model.UndoLast();

                console.log(JSON.stringify(undoneImage))
                await this.view.loadImage(undoneImage.imagepath)
            } catch(err) {
                this.view.errorMessage(err);
            }
        });
    }

    async initializeRelated() {
        document.getElementById("related").addEventListener("click", async (evt) => {
            evt.preventDefault();
            try {
                let imagepathBase = document.getElementById("imgid").src
                let imagepath = imagepathBase.substring(imagepathBase.lastIndexOf("/")+1);

                let image = ({
                    "imagepath": imagepath,
                    "related": true,
                    "annotated": true
                })

                await this.model.imageAnnotate(imagepath, image)

                let nextImage = await this.model.imageRead(1, null, false);

                await this.view.loadImage(nextImage[0].imagepath)
            } catch(err) {
                this.view.errorMessage(err);
            }
        });
    }
    
    async initializeNotRelated() {
        document.getElementById("notrelated").addEventListener("click", async (evt) => {
            evt.preventDefault();
            try {
                let imagepathBase = document.getElementById("imgid").src
                let imagepath = imagepathBase.substring(imagepathBase.lastIndexOf("/")+1);

                let image = ({
                    "imagepath": imagepath,
                    "related": false,
                    "annotated": false
                })

                await this.model.imageAnnotate(imagepath, image)

                let nextImage = await this.model.imageRead(1, null, false);

                await this.view.loadImage(nextImage[0].imagepath)
            } catch(err) {
                this.view.errorMessage(err);
            }
        });
    }
}

// Create the MVC components
const model = new Model();
const view = new View();
const controller = new Controller(model, view);

// export the MVC components as the default
export default {
    model,
    view,
    controller
};