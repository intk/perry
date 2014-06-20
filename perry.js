var fs = require('fs'),
    torrentStream = require('torrent-stream'),
    async = require('async');

var downloadsDir = './downloads';

if (!fs.existsSync(downloadsDir) || !fs.statSync(downloadsDir).isDirectory()) {
    fs.mkdirSync(downloadsDir);
}


if (process.argv.length != 3) {
    console.info("Usage: node peery.js \"magnet:link\"");
} else {
    var magnet = process.argv[2];
    console.info("Downloading magnet link '%s'", magnet);
    //var link = "magnet:?xt=urn:btih:d50a3e9abbe64896bad438e757bd70b54d666173&dn=Bioinformtics%20and%20functional%20genomics.pdf&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337";

    var engine = torrentStream(magnet, {});

    engine
        .on('ready', function() {
            console.info("engine is ready. files:", engine.files.map(function(f) { return f.name }));
            engine.files.forEach(function(file) {
                console.log('downloading %s', file.name);
                var stream = file.createReadStream();
                var wstream = fs.createWriteStream('./' + downloadsDir + '/' + file.name);

                stream.pipe(wstream)
                    .on("finish", function() {
                        console.info('file %s downloaded', file.name);
                        stream.unpipe(wstream);
                        wstream.end()
                    });

                // stream is readable stream to containing the file content
            });
            engine.destroy()
        })
        .on('download', function(index) {  // done
            console.log('file %s downloaded in the background', engine.files[index]);
        });
}
