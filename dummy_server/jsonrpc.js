var rpc = require("json-rpc2");

var server = rpc.Server.$create({
  websocket: true, // is true by default
  headers: {
    // allow custom headers is empty by default
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,PUT,POST,DELETE,OPTIONS",
    "Access-Control-Allow-Headers":
      "Content-Type, Authorization, Content-Length, X-Requested-With"
  }
});

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

function icx_call(args, opt, callback) {
  console.log("CALL");
  console.log(args);
  //  console.log(typeof args.dataType);
  //  if (args.dataType === 'call') {
  let method = args.data.method;
  let params = args.data.params;

  console.log("method:", method);
  console.log("params", params);

  let return_json_str = "";

  switch (method) {
    case "getLastBlock":
      return_json_str = '{"blocknumber":"0x57473"}';
      break;

    case "getBlock":
      return_json_str = `
{
        "version": "0.1a",
        "prev_block_hash": "48757af881f76c858890fb41934bee228ad50a71707154a482826c39b8560d4b",
        "merkle_tree_root_hash": "fabc1884932cf52f657475b6d62adcbce5661754ff1a9d50f13f0c49c7d48c0c",
        "time_stamp": 1516498781094,
        "confirmed_transaction_list": [
            {
                "version": "0x3",
                "from": "hxbe258ceb872e08851f1f59694dac2558708ece11",
                "to": "cxb0776ee37f5b45bfaea8cff1d8232fbb6122ec32",
                "value": "0xde0b6b3a7640000",
                "stepLimit": "0x12345",
                "timestamp": "0x563a6cf330136",
                "nid": "0x3",
                "nonce": "0x1",
                "signature": "VAia7YZ2Ji6igKWzjR2YsGa2m53nKPrfK7uXYW78QLE+ATehAVZPC40szvAiA6NEU5gCYB4c4qaQzqDh2ugcHgA=",
                "txHash": "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238",
                "dataType": "call",
                "data": {
                    "method": "transfer",
                    "params": {
                        "to": "hxab2d8215eab14bc6bdd8bfb2c8151257032ecd8b",
                        "value": "0x1"
                    }
                }
            }
        ],
        "block_hash": "1fcf7c34dc875681761bdaa5d75d770e78e8166b5c4f06c226c53300cbe85f57",
        "height": 3,
        "peer_id": "hx86aba2210918a9b116973f3c4b27c41a54d5dafe",
        "signature": "MEQCICT8mTIL6pRwMWsJjSBHcl4QYiSgG8+0H3U32+05mO9HAiBOhIfBdHNm71WpAZYwJWwQbPVVXFJ8clXGKT3ScDWcvw=="
    }
`;
      break;

    case "getStake":
      return_json_str = `
{
    "stake": "0xde0b6b3a7640000",
    "unstake": "0xde0b6b3a7640000",
    "unstakeBlockHeight": "0xa",
    "blockHeight": "0xa"
}`;
      break;

    case "getDelegation":
      return_json_str = `
{
    "totalDelegated": "0xa688906bd8b0000",
    "votingPower": "0x3782dace9d90000",
    "delegations": [
        {
            "address": "hx1d6463e4628ee52a7f751e9d500a79222a7f3935",
            "value": "0x3782dace9d90000"
        },
        {
            "address": "hxb6bc0bf95d90cb3cd5b3abafd9682a62f36cc826",
            "value": "0x6f05b59d3b20000"
        }
    ]
}`;
      break;

    case "queryIScore":
      return_json_str = `
{
    "blockHeight": "0x10",
    "iscore": "0x3e8",
    "estimatedICX": "0x1"
}`;
      break;

    case "getProposal":
      return_json_str = `{
        "id" : "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238",
        "proposer" : "hxbe258ceb872e08851f1f59694dac2558708ece11",
        "proposerName" : "Icon Foundation",
        "status" : "0x0",
        "startBlockHeight" : "0x1",
        "endBlockHeight" : "0x65",
        "vote": {
            "agree": {
                "list": [{
                    "id": "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238",
                    "timestamp": "0x563a6cf330136",
                    "address": "hxe7af5fcfd8dfc67530a01a0e403882687528dfcb",
                    "name": "Icon Foundation",
                    "amount": "0x1"
                },
                {
                    "id": "0xb903239f8d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238",
                    "timestamp": "0x563a6cf360000",
                    "address": "hxe7af5fcfd8ff67300affffe403882687528dfcb",
                    "name": "My, MY, MY",
                    "amount": "0x3030"
                }
              ],
              "amount": "0x12345"
            },
            "disagree": {
                "list": [{
                    "id": "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238",
                    "timestamp": "0x563a6cf330136",
                    "address": "hxe7af5fcfd8dfc67530a01a0e403882687528dfcb",
                    "name": "Icon Foundation",
                    "amount": "0x2"
                },{
                    "id": "0xb903239f8543d04bc1ba6579132b130876ffff8db1b2dbbf168786408fcbce568238",
                    "timestamp": "0x563b6cf330136",
                    "address": "hxe7af5ffd8fc673bbbbb0a01a0e403882687528dfcb",
                    "name": "NaNaNa",
                    "amount": "0x100"
                }
              ],
              "amount": "0x123"
            },
            "noVote": {
              "list": ["hx31258ceb872e08851f1f59694dac2558708ece11", "hx31258ceb872e08851f1f59694dac2558708eceff"],
              "amount": "0x12312341234a"
            }
        },
        "contents": {
            "title": "Disqualify P-Rep A",
            "description": "P-Rep A does not maintain node",
            "type": "0x1",
            "value": {
                "address": "hxbe258ceb872e08851f1f59694dac2558708ece11"
            }
        }
    }`;
      break;

    case "getProposals":
      return_json_str = `{
      "proposals" : 
      [
            {
                "id" : "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce561111",
                "proposer" : "hxbe258ceb872e08851f1f59694dac2558708ece11",
                "proposerName" : "Icon Foundation",
                "status" : "0x0",
                "startBlockHeight" : "0x1",
                "endBlockHeight" : "0x65",
                "vote": {
                    "agree": {
                        "count": "0x112412349f",
                        "amount": "0x123134123a"
                    },
                    "disagree": {
                        "count": "0x1f98441234",
                        "amount": "0x1312341234"
                    },
                    "noVote": {
                        "count": "0x1343234123a",
                        "amount": "0x2312341234a"
                    }
                },
                "contents": {
                    "title": "MyTextTitle",
                    "description": "Description11111111111",
                    "type": "0x0",
                    "value": {
                        "address": "TextMessage for Text Proposal"
                    }
                }
            },{
                "id" : "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce563333",
                "proposer" : "hxbe258ceb872e08851f1f59694dac2558708ece11",
                "proposerName" : "MyMyMyMy",
                "status" : "0x1",
                "startBlockHeight" : "0x1",
                "endBlockHeight" : "0x65",
                "vote": {
                    "agree": {
                        "count": "0x1",
                        "amount": "0x312341234a"
                    },
                    "disagree": {
                        "count": "0x1",
                        "amount": "0x122341234a"
                    },
                    "noVote": {
                        "count": "0x1",
                        "amount": "0x223141234a"
                    }
                },
                "contents": {
                    "title": "Revision Update",
                    "description": "I want to insert description",
                    "type": "0x1",
                    "value": {
                        "code": 33,
                        "name": "revision Name"
                    }
                }
            },{
                "id" : "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce562222",
                "proposer" : "hxbe258ceb872e08851f1f59694dac2558708ece11",
                "proposerName" : "Nararararara",
                "status" : "0x2",
                "startBlockHeight" : "0x1",
                "endBlockHeight" : "0x65",
                "vote": {
                    "agree": {
                        "count": "0x1",
                        "amount": "0x2312341234a"
                    },
                    "disagree": {
                        "count": "0x1",
                        "amount": "0x1232341234a"
                    },
                    "noVote": {
                        "count": "0x1",
                        "amount": "0x42312341234a"
                    }
                },
                "contents": {
                    "title": "Malicious SCORE Title",
                    "description": "Decription field is where",
                    "type": "0x2",
                    "value": {
                        "address": "hxbe258ceb872e08851f1f59694dac2558708ece11",
                        "type": "0x0"
                    }
                }
            },{
                "id" : "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce563333",
                "proposer" : "hxbe258ceb872e08851f1f59694dac2558708ece11",
                "proposerName" : "Nuguya",
                "status" : "0x0",
                "startBlockHeight" : "0x1",
                "endBlockHeight" : "0x65",
                "vote": {
                    "agree": {
                        "count": "0x1",
                        "amount": "0x52312341234a"
                    },
                    "disagree": {
                        "count": "0x1",
                        "amount": "0x22312341234a"
                    },
                    "noVote": {
                        "count": "0x1",
                        "amount": "0x12312341234a"
                    }
                },
                "contents": {
                    "title": "PRep DisqualificationTitle",
                    "description": "PRep AAA is bad guy",
                    "type": "0x3",
                    "value": {
                        "address": "hxbe258ceb872e08851f1f59694dac2558708ece11"
                    }
                }
            },{
                "id" : "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce564444",
                "proposer" : "hxbe258ceb872e08851f1f59694dac2558708ece11",
                "proposerName" : "OhMy",
                "status" : "0x0",
                "startBlockHeight" : "0x1",
                "endBlockHeight" : "0x65",
                "vote": {
                    "agree": {
                        "count": "0x1",
                        "amount": "0x2312341234a"
                    },
                    "disagree": {
                        "count": "0x1",
                        "amount": "0x1232341234a"
                    },
                    "noVote": {
                        "count": "0x1",
                        "amount": "0x6312341234a"
                    }
                },
                "contents": {
                    "title": "StepPriceTitle",
                    "description": "I want more step Price",
                    "type": "0x4",
                    "value": {
                        "value": "0x10000"
                    }
                }
            }
        ]
    }`;
      break;

    case "getPRep":
      let aRandom = getRandomInt(0, 4);
      switch (aRandom) {
        case 0:
          return_json_str = `{
    "status": "0x0",
    "grade": "0x2",
    "name": "banana",
    "country": "KOR",
    "city": "Seoul",
    "email": "banana@email.com",
    "website": "https://icon.banana.com",
    "details": "https://icon.banana.com/json",
    "p2pEndpoint": "123.45.67.89:7100",
    "publicKey": "0x04abcd8e137f",
    "irep": "0x2000",
    "irepUpdateBlockHeight": "0x847ea",
    "stake": "0x38372",
    "delegated": "0x74287392847",
    "totalBlocks": "0x83261e7",
    "validatedBlocks": "0x83258a9"
}`;
        case 1:
          return_json_str = `{
    "status": "0x0",
    "grade": "0x2",
    "name": "banana111",
    "country": "KOR",
    "city": "Seoul",
    "email": "banana111@email.com",
    "website": "https://icon.banana111.com",
    "details": "https://icon.banana111.com/json",
    "p2pEndpoint": "1.45.67.89:7100",
    "publicKey": "0x04abcd8e137f",
    "irep": "0x2000",
    "irepUpdateBlockHeight": "0x84711",
    "stake": "0x38311",
    "delegated": "0x74287392811",
    "totalBlocks": "0x8326111",
    "validatedBlocks": "0x8325811"
}`;
        case 2:
          return_json_str = `{
    "status": "0x0",
    "grade": "0x2",
    "name": "banana22",
    "country": "KOR",
    "city": "Seoul",
    "email": "banana22@email.com",
    "website": "https://icon.banana22.com",
    "details": "https://icon.banana22.com/json",
    "p2pEndpoint": "12.45.67.89:7100",
    "publicKey": "0x04abcd8e1322",
    "irep": "0x2022",
    "irepUpdateBlockHeight": "0x84722",
    "stake": "0x38322",
    "delegated": "0x74287392822",
    "totalBlocks": "0x8326122",
    "validatedBlocks": "0x8325822"
}`;
        case 3:
          return_json_str = `{
    "status": "0x0",
    "grade": "0x2",
    "name": "banana33",
    "country": "KOR",
    "city": "Seoul",
    "email": "banana33@email.com",
    "website": "https://icon.banana33.com",
    "details": "https://icon.banana33.com/json",
    "p2pEndpoint": "123.45.67.9:7100",
    "publicKey": "0x04abcd8e1333",
    "irep": "0x2033",
    "irepUpdateBlockHeight": "0x84733",
    "stake": "0x38333",
    "delegated": "0x74287392833",
    "totalBlocks": "0x8326133",
    "validatedBlocks": "0x8325833"
}`;
        case 4:
          return_json_str = `{
    "status": "0x0",
    "grade": "0x2",
    "name": "banana44",
    "country": "KOR",
    "city": "Seoul",
    "email": "banana44@email.com",
    "website": "https://icon.banana44.com",
    "details": "https://icon.banana44.com/json",
    "p2pEndpoint": "123.45.67.44:7100",
    "publicKey": "0x04abcd8e1344",
    "irep": "0x2044",
    "irepUpdateBlockHeight": "0x84744",
    "stake": "0x38344",
    "delegated": "0x74287392844",
    "totalBlocks": "0x8326144",
    "validatedBlocks": "0x8325844"
}`;
        default:
          return_json_str = `{
    "status": "0x0",
    "grade": "0x2",
    "name": "defaultbnn",
    "country": "KOR",
    "city": "defoul",
    "email": "defana@email.com",
    "website": "https://icon.default.com",
    "details": "https://icon.default.com/json",
    "p2pEndpoint": "123.45.7.89:7100",
    "publicKey": "0x04abcd8e137f",
    "irep": "0x2000",
    "irepUpdateBlockHeight": "0x847ea",
    "stake": "0x38372",
    "delegated": "0x74280392800",
    "totalBlocks": "0x8326000",
    "validatedBlocks": "0x8325800"
}`;
      }
      break;

    case "getPReps":
      return_json_str = `{
        "blockHeight": "0x1234",
        "startRanking": "0x1",
        "totalDelegated": "0x2863c1f5cdae42f9540000000",
        "totalStake": "0x193e5939a08ce9dbd480000000",
        "preps": [
            {
                "name": "Banana node",
                "country": "KOR",
                "city": "Seoul",
                "grade": "0x0",
                "address": "hx8f21e5c54f006b6a5d5fe65486908592151a7c57",
                "irep": "0xc350",
                "irepUpdateBlockHeight": "0x1200",
                "lastGenerateBlockHeight": "-0x1",
                "stake": "0x21e19e0c9bab2400000",
                "delegated": "0x204fce5e3e25026110000000",
                "totalBlocks": "0x2710",
                "validatedBlocks": "0x2328"
            },
            {
                "name": "ABC Node",
                "country": "USA",
                "city": "New York",
                "grade": "0x0",
                "address": "hx1d6463e4628ee52a7f751e9d500a79222a7f3935",
                "irep": "0xc350",
                "irepUpdateBlockHeight": "0x1100",
                "lastGenerateBlockHeight": "0x1200",
                "stake": "0x28a857425466f800000",
                "delegated": "0x9ed194db19b238c000000",
                "totalBlocks": "0x2720",
                "validatedBlocks": "0x2348"
            },
            {
                "name": "TEST Node",
                "country": "KR",
                "city": "Seoul",
                "grade": "0x0",
                "address": "hx1d6463e4628ee52a7f751e9d500a79222a7f3935",
                "irep": "0xc350",
                "irepUpdateBlockHeight": "0x1100",
                "lastGenerateBlockHeight": "0x1200",
                "stake": "0x28a857425466f800000",
                "delegated": "0x9ed194db19b238c000000",
                "totalBlocks": "0x2720",
                "validatedBlocks": "0x2348"
            },
            {
                "name": "ASDFASDF Node",
                "country": "USA",
                "city": "New York",
                "grade": "0x0",
                "address": "hx1d6463e4628ee52a7f751e9d500a79222a7f3935",
                "irep": "0xc350",
                "irepUpdateBlockHeight": "0x1100",
                "lastGenerateBlockHeight": "0x1200",
                "stake": "0x28a857425466f800000",
                "delegated": "0x9ed194db19b238c000000",
                "totalBlocks": "0x2720",
                "validatedBlocks": "0x2348"
            },
            {
                "name": "raynear Node",
                "country": "JPN",
                "city": "New York",
                "grade": "0x0",
                "address": "hx1d6463e4628ee52a7f751e9d500a79222a7f3935",
                "irep": "0xc350",
                "irepUpdateBlockHeight": "0x1100",
                "lastGenerateBlockHeight": "0x1200",
                "stake": "0x28a857425466f800000",
                "delegated": "0x9ed194db19b238c000000",
                "totalBlocks": "0x2720",
                "validatedBlocks": "0x2348"
            },
            {
                "name": "myname Node",
                "country": "CHN",
                "city": "New York",
                "grade": "0x0",
                "address": "hx1d6463e4628ee52a7f751e9d500a79222a7f3935",
                "irep": "0xc350",
                "irepUpdateBlockHeight": "0x1100",
                "lastGenerateBlockHeight": "0x1200",
                "stake": "0x28a857425466f800000",
                "delegated": "0x9ed194db19b238c000000",
                "totalBlocks": "0x2720",
                "validatedBlocks": "0x2348"
            }
        ]
}`;
      break;

    default:
      break;
  }

  console.log(return_json_str);

  let return_json = JSON.parse(return_json_str);

  callback(null, return_json);
  //  }
}
server.expose("icx_call", icx_call);

function icx_sendTransaction(args, opt, callback) {
  console.log("sendTransaction!!");
  console.log(args);
  //  console.log(typeof args.dataType);

  let method = args.data.method;
  let params = args.data.params;

  console.log("method:", method);
  console.log("params:", params);

  let return_json_str = "";

  switch (method) {
    case "setStake":
      return_json_str = '{"txhash":"khi238hkljsdfhlkadsfjlkserjlk23rjoiedhf"}';
      break;

    case "setDelegate":
      return_json_str = '{"txhash":"khi238hkljsdfhlkadsfjlkserjlk23rjoiedhf"}';
      break;

    case "claimIScore":
      console.log("IScoreClaimed(int, int):sdjfvhbiu2h34r....(signature)");
      console.log("I-Score:348598");
      console.log("ICX:398");

      return_json_str = "{}";
      break;

    case "registerPRep":
      console.log(
        "PRepRegistered(hx8239432db3db):v48nc94nhfcv3948cnhf..(signature)"
      );
      console.log("Address:hx8239432db3db");

      return_json_str = '{"txhash":"khi238hkljsdfhlkadsfjlkserjlk23rjoiedhf"}';
      break;
    case "unregisterPRep":
      console.log(
        "PRepUnregistered(hx8239432db3db):v48nc94nhfcv3948cnhf..(signature)"
      );
      console.log("Address:hx8239432db3db");

      return_json_str = '{"txhash":"khi238hkljsdfhlkadsfjlkserjlk23rjoiedhf"}';
      break;
    case "setPRep":
      console.log("PRepSet(hx8239432db3db):v48nc94nhfcv3948cnhf..(signature)");
      console.log("Address:hx8239432db3db");

      return_json_str = '{"txhash":"khi238hkljsdfhlkadsfjlkserjlk23rjoiedhf"}';
      break;

    case "setGovernanceVariables":
      return_json_str = '{"txhash":"khi238hkljsdfhlkadsfjlkserjlk23rjoiedhf"}';
      break;

    case "registerProposal":
      switch (parseInt(args.type)) {
        case 0:
          console.log("NetworlProposal: Text Proposal");
          break;
        case 1:
          console.log("NetworlProposal: Revision update Proposal");
          break;
        case 2:
          console.log("NetworlProposal: Malicious SCORE Proposal");
          break;
        case 3:
          console.log("NetworlProposal: P-Rep disqualification Proposal");
          break;
        case 4:
          console.log("NetworlProposal: Step price Proposal");
          break;
        default:
          console.log("Error");
          break;
      }
      return_json_str = `{
      "txhash":"registerProposalkhi238hkljsdfhlkadsfjlkserjlk23rjoiedhf"
}`;
      break;

    case "cancelProposal":
      return_json_str = `{
      "txhash":"registerProposalkhi238hkljsdfhlkadsfjlkserjlk23rjoiedhf"
}`;
      break;

    case "voteProposal":
      return_json_str = `{
      "txhash":"registerProposalkhi238hkljsdfhlkadsfjlkserjlk23rjoiedhf"
}`;
      break;

    default:
      console.log("default");
      break;
  }

  console.log(return_json_str);

  let return_json = JSON.parse(return_json_str);
  console.log("return", return_json);
  callback(null, return_json);
  //  }
}
server.expose("icx_sendTransaction", icx_sendTransaction);

server.listen(8888, "localhost");
//server.listen(8888, "192.168.99.1");
