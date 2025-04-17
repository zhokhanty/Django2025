<template>
    <div> 
      <h1>Resumes</h1> 
      <ul> 
        <li v-for="resume in resumes" :key="resume.id"> 
          {{ resume.file }} - {{ resume.uploaded_at }} 
        </li> 
      </ul> 
      <form @submit.prevent="addResume"> 
        <input v-model="newResume.file" placeholder="File" required /> 
        <input v-model="newResume.uploaded_at" placeholder="Uploaded at" required /> 
        <button type="submit">Add Resume</button> 
      </form> 
    </div> 
  </template> 
  
  <script> 

  import { getResumes, createResume } from '../api'; 
  
  export default { 
    data() { 
      return { 
        resumes: [], 
        newResume: { file: '', uploaded_at: '' }, 
      }; 
    },
    async created() { 
      this.resumes = await getResumes(); 
    }, 
  
    methods: { 
      async addResume() { 
        const resume = await createResume(this.newResume); 
        this.resumes.push(resume); 
        this.newResume = { file: '', uploaded_at: '' }; 
      }, 
    }, 
  }; 
  </script> 