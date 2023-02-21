<template>
    <v-container fluid>
        <div justify="center" vertical-align="top">
            <h1>Feedback</h1>
            <p>Thanks for taking time to give us feedback! It helps us make this application better.</p>

            <v-spacer></v-spacer>

            <h4>Please rate this application from 1 - 10.</h4>
            <v-rating
                color="primary"
                empty-icon="mdi-star-outline"
                full-icon="mdi-star"
                half-icon="mdi-star-half-full"
                hover
                length="5"
                size="32"
                value="3"
            ></v-rating>

            <br>

            <h4>Anything else you would like to say?</h4>

            <v-textarea
                color="primary"
                hint="Enter any additional comments here, like how can we improve"
                name="input-feedback"
            ></v-textarea>

            <br>

            <v-btn color="primary">
                Submit Feedback
            </v-btn>
        </div>
    </v-container>
</template>

<script>
</script>

<style scoped>

</style>
