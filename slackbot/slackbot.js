let { Botkit } = require('botkit');

const { SlackAdapter } = require('botbuilder-adapter-slack');

const dotenv = require('dotenv');
// Import required bot configuration.
const ENV_FILE = ('.env');
dotenv.config({ path: ENV_FILE });

const adapter = new SlackAdapter({
    // // REMOVE THIS OPTION AFTER YOU HAVE CONFIGURED YOUR APP!
    // enable_incomplete: true,

    // parameters used to secure webhook endpoint
    verificationToken: process.env.VERIFICATION_TOKEN,
    clientSigningSecret: process.env.CLIENT_SIGNING_SECRET,  

    // auth token for a single-team app
    botToken: process.env.BOT_TOKEN,

    
});

const controller = new Botkit({
    adapter,
    // ...other options
});



controller.on('channel_join', async(bot) => {
    bot.reply('i am here');
});

controller.on('message', async(bot, message) => {
    await bot.reply(message, 'I heard a message!');
    console.log('messaged')
});

controller.hears('hello','direct_message', function(bot, message) {
    console.log('hello')
    bot.reply(message,'Hello yourself!');
});
